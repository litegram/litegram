from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from litestar import Request, Response
from litestar.response import File as FileResponse

from litegram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    WebAppInfo,
)
from litegram.utils.web_app import check_webapp_signature, safe_parse_webapp_init_data

if TYPE_CHECKING:
    from litegram import Bot


async def demo_handler(request: Request) -> FileResponse:
    return FileResponse(path=Path(__file__).parent.resolve() / "demo.html")


async def check_data_handler(request: Request) -> Response:
    bot: Bot = request.app.state.bot

    data = await request.form()
    if check_webapp_signature(bot.token, data["_auth"]):
        return Response({"ok": True})
    return Response({"ok": False, "err": "Unauthorized"}, status_code=401)


async def send_message_handler(request: Request) -> Response:
    bot: Bot = request.app.state.bot
    data = await request.form()
    try:
        web_app_init_data = safe_parse_webapp_init_data(token=bot.token, init_data=data["_auth"])
    except ValueError:
        return Response({"ok": False, "err": "Unauthorized"}, status_code=401)

    reply_markup = None
    if data["with_webview"] == "1":
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Open",
                        web_app=WebAppInfo(
                            url=str(request.url.with_replacements(scheme="https", path="demo")),
                        ),
                    ),
                ],
            ],
        )
    await bot.answer_web_app_query(
        web_app_query_id=web_app_init_data.query_id,
        result=InlineQueryResultArticle(
            id=web_app_init_data.query_id,
            title="Demo",
            input_message_content=InputTextMessageContent(
                message_text="Hello, World!",
                parse_mode=None,
            ),
            reply_markup=reply_markup,
        ),
    )
    return Response({"ok": True})
