"""Behavioral tests for sendWidget (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendRichMessage, SendWidget
from litegram.types import Chat, InputRichBlockParagraph, InputRichMessage, Message, RichTextBold

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendWidget:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendWidget,
            ok=True,
            result=Message(message_id=42, date=datetime.datetime.now(datetime.UTC), chat=Chat(id=42, type="private"), text="test"),
        )

        response = await bot.send_widget(chat_id=42, html="<b>test</b>")
        assert isinstance(bot.get_request(), SendWidget)
        assert response == prepare_result.result


def test_rich_text_in_method() -> None:
    method = SendRichMessage(
        chat_id=42,
        rich_message=InputRichMessage(blocks=[InputRichBlockParagraph(text=RichTextBold(text="x"))]),
    )
    assert method.rich_message.model_dump(exclude_none=True)["blocks"][0]["text"]["type"] == "bold"
