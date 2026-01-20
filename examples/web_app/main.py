from __future__ import annotations

import logging
import sys
from os import getenv
from typing import Any

import uvicorn
from litestar import Litestar, Request, get, post
from litestar.datastructures import State
from litestar.di import Provide

from handlers import my_router
from litegram import Bot, Dispatcher
from litegram.client.default import DefaultBotProperties
from litegram.enums.parse_mode import ParseMode
from litegram.types import MenuButtonWebApp, Update, WebAppInfo
from litegram.webhook.litestar_server import webhook_handler
from routes import check_data_handler, demo_handler, send_message_handler

TOKEN = getenv("BOT_TOKEN")

APP_BASE_URL = getenv("APP_BASE_URL")


async def on_startup(bot: Bot, base_url: str) -> None:
    await bot.set_webhook(f"{base_url}/webhook")
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="Open Menu", web_app=WebAppInfo(url=f"{base_url}/demo")),
    )


def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher()
    dispatcher["base_url"] = APP_BASE_URL
    dispatcher.startup.register(on_startup)

    dispatcher.include_router(my_router)

    @get("/demo")
    async def demo(request: Request) -> Any:
        return await demo_handler(request)

    @post("/demo/checkData")
    async def check_data(request: Request) -> Any:
        return await check_data_handler(request)

    @post("/demo/sendMessage")
    async def send_message(request: Request) -> Any:
        return await send_message_handler(request)

    # And finally start webserver
    app = Litestar(
        route_handlers=[post("/webhook")(webhook_handler), demo, check_data, send_message],
        dependencies={
            "bot": Provide(lambda: bot),
            "dispatcher": Provide(lambda: dispatcher),
        },
        on_startup=[lambda: dispatcher.emit_startup(bot=bot, base_url=APP_BASE_URL)],
        on_shutdown=[lambda: dispatcher.emit_shutdown(bot=bot, base_url=APP_BASE_URL), bot.session.close],
        state=State({"bot": bot}),
    )

    uvicorn.run(app, host="127.0.0.1", port=8081)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
