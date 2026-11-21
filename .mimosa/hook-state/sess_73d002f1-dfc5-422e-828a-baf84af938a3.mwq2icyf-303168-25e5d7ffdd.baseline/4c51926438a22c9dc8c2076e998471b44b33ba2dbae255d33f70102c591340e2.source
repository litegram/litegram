"""Behavioral tests for editMessageWidgetData (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditMessageWidgetData
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditMessageWidgetData:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditMessageWidgetData,
            ok=True,
            result=True,
        )

        response = await bot.edit_message_widget_data()
        bot.get_request()
        assert response == prepare_result.result
