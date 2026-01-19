from __future__ import annotations

import asyncio
import secrets
import warnings
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, cast

from litestar import Request, Response, post
from litestar.background_tasks import BackgroundTask
from litestar.status_codes import HTTP_401_UNAUTHORIZED

from litegram import Bot, Dispatcher
from litegram.types import Update

if TYPE_CHECKING:
    # Removed TelegramType import
    from litegram.methods import TelegramMethod

    pass


class BaseRequestHandler(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        handle_in_background: bool = False,
        **data: Any,
    ) -> None:
        self.dispatcher = dispatcher
        self.handle_in_background = handle_in_background
        self.data = data

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def resolve_bot(self, request: Request) -> Bot:
        pass

    @abstractmethod
    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        pass

    async def _handle_request(self, bot: Bot, update: Update) -> Any:
        result: TelegramMethod[Any] | None = await self.dispatcher.feed_webhook_update(
            bot,
            update,
            **self.data,
        )
        if result:
            return self._format_response(bot=bot, result=result)
        return {}

    def _format_response(self, bot: Bot, result: TelegramMethod[Any]) -> dict[str, Any]:
        data = bot.session.prepare_value(
            result.model_dump(warnings=False),
            bot=bot,
            files={},
            _dumps_json=False,
        )
        return {"method": result.__api_method__, **data}

    async def handle(self, request: Request) -> Any:
        bot = await self.resolve_bot(request)
        if not self.verify_secret(request.headers.get("X-Telegram-Bot-Api-Secret-Token", ""), bot):
            return Response(content="Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

        # In Litestar we can let the route handler take the Update object directly.
        # But for BaseRequestHandler which is often used as a standalone callable,
        # we still support manual parsing.
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})

        if self.handle_in_background:
            return Response(
                content={},
                background=BackgroundTask(
                    self.dispatcher.feed_raw_update,
                    bot=bot,
                    update=update_data,
                    **self.data,
                ),
            )

        return await self._handle_request(bot=bot, update=update)

    __call__ = handle


class SimpleRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        handle_in_background: bool = True,
        secret_token: str | None = None,
        **data: Any,
    ) -> None:
        super().__init__(dispatcher=dispatcher, handle_in_background=handle_in_background, **data)
        self.bot = bot
        self.secret_token = secret_token

    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        if self.secret_token:
            return secrets.compare_digest(telegram_secret_token, self.secret_token)
        return True

    async def close(self) -> None:
        await self.bot.session.close()

    async def resolve_bot(self, request: Request) -> Bot:
        return self.bot


class TokenBasedRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        handle_in_background: bool = True,
        bot_settings: dict[str, Any] | None = None,
        **data: Any,
    ) -> None:
        super().__init__(dispatcher=dispatcher, handle_in_background=handle_in_background, **data)
        if bot_settings is None:
            bot_settings = {}
        self.bot_settings = bot_settings
        self.bots: dict[str, Bot] = {}

    def verify_secret(self, telegram_secret_token: str, bot: Bot) -> bool:
        return True

    async def close(self) -> None:
        for bot in self.bots.values():
            await bot.session.close()

    async def resolve_bot(self, request: Request) -> Bot:
        token = request.path_parameters["bot_token"]
        if token not in self.bots:
            self.bots[token] = Bot(token=token, **self.bot_settings)
        return self.bots[token]


async def webhook_handler(
    data: Update | dict[str, Any],
    request: Request,
    dispatcher: Dispatcher,
    bot: Bot,
    **kwargs: Any,
) -> Any:
    """
    Optimized Litestar-native webhook handler.
    To use this, bot and dispatcher should be provided via DI or app state.
    """
    secret_token = kwargs.get("secret_token")
    if secret_token:
        token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if not token or not secrets.compare_digest(token, secret_token):
            return Response(content="Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    if isinstance(data, dict):
        data = Update.model_validate(data, context={"bot": bot})
    else:
        # Re-mount bot to update context
        data._bot = bot

    if kwargs.get("handle_in_background", False):
        return Response(
            content={},
            background=BackgroundTask(
                dispatcher.feed_update,
                bot=bot,
                update=data,
            ),
        )

    result = await dispatcher.feed_webhook_update(bot, data)
    if result:
        res_data = bot.session.prepare_value(
            result.model_dump(warnings=False),
            bot=bot,
            files={},
            _dumps_json=False,
        )
        return {"method": result.__api_method__, **res_data}
    return {}
