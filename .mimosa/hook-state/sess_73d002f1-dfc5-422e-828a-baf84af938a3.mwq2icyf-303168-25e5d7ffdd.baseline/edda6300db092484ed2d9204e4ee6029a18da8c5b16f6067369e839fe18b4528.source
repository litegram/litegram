"""Behavioral tests for getManagedBotAccessSettings (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetManagedBotAccessSettings
from litegram.types import BotAccessSettings, Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetManagedBotAccessSettings:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetManagedBotAccessSettings,
            ok=True,
            result=BotAccessSettings(is_access_restricted=False),
        )

        response = await bot.get_managed_bot_access_settings(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
