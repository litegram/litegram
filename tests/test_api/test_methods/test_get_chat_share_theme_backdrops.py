"""Behavioral tests for getChatShareThemeBackdrops (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetChatShareThemeBackdrops
from litegram.types import Chat, ChatShareThemeBackdrops, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetChatShareThemeBackdrops:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetChatShareThemeBackdrops,
            ok=True,
            result=ChatShareThemeBackdrops(backdrops=[]),
        )

        response = await bot.get_chat_share_theme_backdrops()
        bot.get_request()
        assert response == prepare_result.result
