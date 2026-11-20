"""Tests for sendWidget (Bot API 10.4) and sendRichMessage (Bot API 10.0)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import AnswerWidgetQuery, SendRichMessage, SendWidget
from litegram.types import Chat, Message, RichMessage, RichTextBold

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendWidget:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendWidget,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                text="widget",
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_widget(
            chat_id=42,
            html="<b>hello</b>",
        )
        bot.get_request()
        assert response == prepare_result.result


class TestSendRichMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        rich = RichMessage(blocks=[{"type": "paragraph", "text": "hello"}])
        prepare_result = bot.add_result_for(
            SendRichMessage,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                text="rich",
                chat=Chat(id=42, type="private"),
                rich_message=rich,
            ),
        )

        response: Message = await bot.send_rich_message(
            chat_id=42,
            rich_message={"blocks": [{"type": "paragraph", "text": "hello"}]},
        )
        bot.get_request()
        assert response == prepare_result.result

    def test_rich_text_in_method(self):
        method = SendRichMessage(
            chat_id=42,
            rich_message={"blocks": [{"type": "paragraph", "text": RichTextBold(text="x")}]},
        )
        assert method.rich_message is not None


class TestAnswerWidgetQuery:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            AnswerWidgetQuery,
            ok=True,
            result=True,
        )
        response = await bot.answer_widget_query(widget_query_id="q1")
        bot.get_request()
        assert response == prepare_result.result
