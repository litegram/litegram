"""Behavioral tests for getUserProfileAudios (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetUserProfileAudios
from litegram.types import Chat, Message, UserProfileAudios

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetUserProfileAudios:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetUserProfileAudios,
            ok=True,
            result=UserProfileAudios(total_count=0, audios=[]),
        )

        response = await bot.get_user_profile_audios(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
