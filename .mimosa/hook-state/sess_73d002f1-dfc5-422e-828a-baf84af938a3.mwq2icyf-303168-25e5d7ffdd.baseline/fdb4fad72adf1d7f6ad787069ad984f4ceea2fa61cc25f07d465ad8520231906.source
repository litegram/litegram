from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendMessage
from litegram.types import Chat, ForceReply, Message, ReplyKeyboardRemove

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendMessage,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                text="test",
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_message(chat_id=42, text="test")
        bot.get_request()
        assert response == prepare_result.result

    @pytest.mark.anyio
    async def test_force_reply(self):
        # https://github.com/litegram/litegram/issues/901
        method = SendMessage(text="test", chat_id=42, reply_markup=ForceReply())
        assert isinstance(method.reply_markup, ForceReply)

    @pytest.mark.anyio
    async def test_reply_keyboard_remove(self):
        # https://github.com/litegram/litegram/issues/901
        method = SendMessage(text="test", chat_id=42, reply_markup=ReplyKeyboardRemove())
        assert isinstance(method.reply_markup, ReplyKeyboardRemove)
