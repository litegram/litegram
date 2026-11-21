"""Behavioral tests for sendChatJoinRequestWebApp (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendChatJoinRequestWebApp
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendChatJoinRequestWebApp:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendChatJoinRequestWebApp,
            ok=True,
            result=True,
        )

        response = await bot.send_chat_join_request_web_app(chat_join_request_query_id="q1", web_app_url="https://example.com")
        bot.get_request()
        assert response == prepare_result.result
