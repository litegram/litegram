"""Behavioral tests for getManagedBotToken (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetManagedBotToken
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetManagedBotToken:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetManagedBotToken,
            ok=True,
            result="token",
        )

        response = await bot.get_managed_bot_token(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
