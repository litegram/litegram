"""Behavioral tests for editEphemeralMessageMedia (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditEphemeralMessageMedia
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditEphemeralMessageMedia:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditEphemeralMessageMedia,
            ok=True,
            result=True,
        )

        response = await bot.edit_ephemeral_message_media(chat_id=42, receiver_user_id=42, ephemeral_message_id=42, media={"type": "photo", "media": "photo-id"})
        bot.get_request()
        assert response == prepare_result.result
