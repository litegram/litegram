"""Behavioral tests for deleteAllMessageReactions (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteAllMessageReactions
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteAllMessageReactions:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            DeleteAllMessageReactions,
            ok=True,
            result=True,
        )

        response = await bot.delete_all_message_reactions(chat_id=42)
        bot.get_request()
        assert response == prepare_result.result
