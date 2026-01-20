from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.client.session.middlewares.base import (
    BaseRequestMiddleware,
    NextRequestMiddlewareType,
)
from litegram.client.session.middlewares.manager import RequestMiddlewareManager

if TYPE_CHECKING:
    from litegram import Bot
    from litegram.methods import Response, TelegramMethod
    from litegram.types import TelegramObject


class TestMiddlewareManager:
    @pytest.mark.anyio
    async def test_register(self):
        manager = RequestMiddlewareManager()

        @manager
        async def middleware(handler, event, data):
            await handler(event, data)

        assert middleware in manager._middlewares
        manager.unregister(middleware)
        assert middleware not in manager._middlewares

    @pytest.mark.anyio
    async def test_wrap_middlewares(self):
        manager = RequestMiddlewareManager()

        class MyMiddleware(BaseRequestMiddleware):
            async def __call__(
                self,
                make_request: NextRequestMiddlewareType,
                bot: Bot,
                method: TelegramMethod[TelegramObject],
            ) -> Response[TelegramObject]:
                return await make_request(bot, method)

        manager.register(MyMiddleware())

        @manager()  # type: ignore
        @manager
        async def middleware(make_request, bot, method):
            return await make_request(bot, method)

        async def target_call(bot, method, timeout: int = None):
            return timeout

        assert await manager.wrap_middlewares(target_call, timeout=42)(None, None) == 42
