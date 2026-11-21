"""Behavioral tests for deleteEphemeralMessage (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteEphemeralMessage
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteEphemeralMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            DeleteEphemeralMessage,
            ok=True,
            result=True,
        )

        response = await bot.delete_ephemeral_message(chat_id=42, receiver_user_id=42, ephemeral_message_id=42)
        bot.get_request()
        assert response == prepare_result.result
