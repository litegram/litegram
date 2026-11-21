from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest
from litestar.background_tasks import BackgroundTask
from litestar.status_codes import HTTP_401_UNAUTHORIZED

from litegram import Dispatcher
from litegram.methods import GetMe
from litegram.webhook.litestar_server import SimpleRequestHandler, webhook_handler

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class FakeRequest:
    def __init__(self, secret: str = "secret") -> None:
        self.headers = {"X-Telegram-Bot-Api-Secret-Token": secret}

    async def json(self) -> dict:
        return {"update_id": 1}


@pytest.mark.anyio
async def test_base_handler_background(bot: MockedBot):
    dispatcher = Dispatcher()
    handler = SimpleRequestHandler(dispatcher=dispatcher, bot=bot, handle_in_background=True)

    response = await handler.handle(FakeRequest())
    assert isinstance(response.background, BackgroundTask)


@pytest.mark.anyio
async def test_simple_handler_close(bot: MockedBot):
    handler = SimpleRequestHandler(dispatcher=Dispatcher(), bot=bot)
    assert await handler.resolve_bot(FakeRequest()) is bot
    await handler.close()
    assert bot.session.closed


@pytest.mark.anyio
async def test_webhook_background_and_secret_rejection(bot: MockedBot):
    dispatcher = Dispatcher()
    dispatcher.feed_webhook_update = AsyncMock(return_value=None)

    response = await webhook_handler(
        data={"update_id": 1},
        request=FakeRequest(secret="wrong"),
        dispatcher=dispatcher,
        bot=bot,
        secret_token="secret",
        handle_in_background=True,
    )
    assert response.status_code == HTTP_401_UNAUTHORIZED

    response = await webhook_handler(
        data={"update_id": 1},
        request=FakeRequest(),
        dispatcher=dispatcher,
        bot=bot,
        secret_token="secret",
        handle_in_background=True,
    )
    assert isinstance(response.background, BackgroundTask)


@pytest.mark.anyio
async def test_webhook_returns_method_and_empty_result(bot: MockedBot):
    dispatcher = Dispatcher()
    dispatcher.feed_webhook_update = AsyncMock(return_value=GetMe())
    result = await webhook_handler(
        data={"update_id": 1},
        request=FakeRequest(),
        dispatcher=dispatcher,
        bot=bot,
    )
    assert result["method"] == "getMe"

    dispatcher.feed_webhook_update = AsyncMock(return_value=None)
    result = await webhook_handler(
        data={"update_id": 1},
        request=FakeRequest(),
        dispatcher=dispatcher,
        bot=bot,
    )
    assert result == {}
