"""Behavioral tests for editSharedWidgetData (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditSharedWidgetData
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditSharedWidgetData:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditSharedWidgetData,
            ok=True,
            result=True,
        )

        response = await bot.edit_shared_widget_data(widget_id="w1", public_data="data")
        bot.get_request()
        assert response == prepare_result.result
