"""Behavioral tests for answerChatJoinRequestQuery (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import AnswerChatJoinRequestQuery
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestAnswerChatJoinRequestQuery:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            AnswerChatJoinRequestQuery,
            ok=True,
            result=True,
        )

        response = await bot.answer_chat_join_request_query(chat_join_request_query_id="q1", result="ok")
        bot.get_request()
        assert response == prepare_result.result
