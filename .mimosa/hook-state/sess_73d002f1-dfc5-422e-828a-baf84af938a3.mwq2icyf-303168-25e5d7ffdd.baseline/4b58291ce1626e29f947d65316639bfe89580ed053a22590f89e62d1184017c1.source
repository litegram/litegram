"""Behavioral tests for answerWidgetQuery (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import AnswerWidgetQuery
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestAnswerWidgetQuery:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            AnswerWidgetQuery,
            ok=True,
            result=True,
        )

        response = await bot.answer_widget_query(widget_query_id="w1")
        bot.get_request()
        assert response == prepare_result.result
