"""Behavioral tests for getUserPersonalChatMessages (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetUserPersonalChatMessages
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetUserPersonalChatMessages:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetUserPersonalChatMessages,
            ok=True,
            result=[Message(message_id=42, date=datetime.datetime.now(datetime.UTC), chat=Chat(id=42, type="private"), text="test")],
        )

        response = await bot.get_user_personal_chat_messages(user_id=42, limit=10)
        bot.get_request()
        assert response == prepare_result.result
