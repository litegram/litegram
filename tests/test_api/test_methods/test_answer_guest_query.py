from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram import Bot
from litegram.client.session.httpx import HttpxSession
from litegram.types import InlineQueryResultArticle, InputTextMessageContent, SentGuestMessage

if TYPE_CHECKING:
    from pytest_httpx import HTTPXMock


@pytest.mark.anyio
async def test_answer_guest_query_decodes_telegram_response(httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://api.telegram.org/bot42:TEST/answerGuestQuery",
        method="POST",
        json={"ok": True, "result": {"inline_message_id": "sent-guest-message"}},
    )
    async with HttpxSession() as session:
        bot = Bot("42:TEST", session=session)
        response = await bot.answer_guest_query(
            guest_query_id="g1",
            result=InlineQueryResultArticle(id="1", title="t", input_message_content=InputTextMessageContent(message_text="x")),
        )
    assert isinstance(response, SentGuestMessage)
    assert response.inline_message_id == "sent-guest-message"
