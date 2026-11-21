"""Behavioral tests for setChatMemberTag (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetChatMemberTag
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetChatMemberTag:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SetChatMemberTag,
            ok=True,
            result=True,
        )

        response = await bot.set_chat_member_tag(chat_id=42, user_id=42)
        bot.get_request()
        assert response == prepare_result.result
