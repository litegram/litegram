from __future__ import annotations

import logging
import sys
from os import getenv
from typing import TYPE_CHECKING, Any

import uvicorn
from litestar import Litestar, Request, post

from litegram import Bot, Dispatcher, F, Router
from litegram.client.session.httpx import HttpxSession
from litegram.enums import ParseMode
from litegram.exceptions import TelegramUnauthorizedError
from litegram.filters import Command, CommandObject
from litegram.fsm.storage.memory import MemoryStorage
from litegram.types import Update
from litegram.utils.token import TokenValidationError, validate_token
from litegram.webhook.litestar_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
)

if TYPE_CHECKING:
    from litegram.types import Message

# In multibot example we usually have multiple routers
# but here we use a simplified version
main_router = Router()

BASE_URL = getenv("BASE_URL", "https://example.com")
MAIN_BOT_TOKEN = getenv("BOT_TOKEN")

WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8080
MAIN_BOT_PATH = "/webhook/main"
OTHER_BOTS_PATH = "/webhook/bot/{bot_token}"

OTHER_BOTS_URL = f"{BASE_URL}{OTHER_BOTS_PATH}"


def is_bot_token(value: str) -> bool | dict[str, Any]:
    try:
        validate_token(value)
    except TokenValidationError:
        return False
    return True


@main_router.message(Command("add", magic=F.args.func(is_bot_token)))
async def command_add_bot(message: Message, command: CommandObject, bot: Bot) -> Any:
    new_bot = Bot(token=command.args, session=bot.session)
    try:
        bot_user = await new_bot.get_me()
    except TelegramUnauthorizedError:
        return message.answer("Invalid token")
    await new_bot.delete_webhook(drop_pending_updates=True)
    await new_bot.set_webhook(OTHER_BOTS_URL.format(bot_token=command.args))
    return await message.answer(f"Bot @{bot_user.username} successful added")


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_URL}{MAIN_BOT_PATH}")


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    session = HttpxSession()
    bot_settings = {"session": session, "parse_mode": ParseMode.HTML}
    bot = Bot(token=MAIN_BOT_TOKEN, **bot_settings)
    storage = MemoryStorage()

    main_dispatcher = Dispatcher(storage=storage)
    main_dispatcher.include_router(main_router)
    main_dispatcher.startup.register(on_startup)

    multibot_dispatcher = Dispatcher(storage=storage)
    # In a real example, we might include other routers here
    # multibot_dispatcher.include_router(form_router)

    main_handler = SimpleRequestHandler(dispatcher=main_dispatcher, bot=bot)
    multibot_handler = TokenBasedRequestHandler(
        dispatcher=multibot_dispatcher,
        bot_settings=bot_settings,
    )

    # And finally start webserver
    app = Litestar(
        route_handlers=[post(MAIN_BOT_PATH)(main_handler), post(OTHER_BOTS_PATH)(multibot_handler)],
        on_startup=[lambda: main_dispatcher.emit_startup(bot=bot)],
        on_shutdown=[
            lambda: main_dispatcher.emit_shutdown(bot=bot),
            bot.session.close,
            multibot_handler.close,
        ],
    )

    uvicorn.run(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
