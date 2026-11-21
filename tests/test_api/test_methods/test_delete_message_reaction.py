"""Behavioral tests for deleteMessageReaction (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteMessageReaction
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteMessageReaction:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            DeleteMessageReaction,
            ok=True,
            result=True,
        )

        response = await bot.delete_message_reaction(chat_id=42, message_id=42)
        bot.get_request()
        assert response == prepare_result.result
