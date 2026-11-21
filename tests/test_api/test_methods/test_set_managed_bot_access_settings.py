"""Behavioral tests for setManagedBotAccessSettings (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetManagedBotAccessSettings
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetManagedBotAccessSettings:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SetManagedBotAccessSettings,
            ok=True,
            result=True,
        )

        response = await bot.set_managed_bot_access_settings(user_id=42, is_access_restricted=False)
        bot.get_request()
        assert response == prepare_result.result
