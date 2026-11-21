"""Behavioral tests for replaceManagedBotToken (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import ReplaceManagedBotToken
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestReplaceManagedBotToken:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            ReplaceManagedBotToken,
            ok=True,
            result="token",
        )

        response = await bot.replace_managed_bot_token(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
