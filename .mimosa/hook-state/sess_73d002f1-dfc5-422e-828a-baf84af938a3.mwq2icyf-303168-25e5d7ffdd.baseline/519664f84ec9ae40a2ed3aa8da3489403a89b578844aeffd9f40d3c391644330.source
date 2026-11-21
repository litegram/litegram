from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import ForwardMessage
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestForwardMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            ForwardMessage,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                chat=Chat(id=42, title="chat", type="private"),
                text="text",
            ),
        )

        response: Message = await bot.forward_message(chat_id=42, from_chat_id=42, message_id=42)
        request = bot.get_request()
        assert request
        assert response == prepare_result.result
