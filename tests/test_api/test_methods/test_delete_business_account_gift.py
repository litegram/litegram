"""Behavioral tests for deleteBusinessAccountGift (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteBusinessAccountGift
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteBusinessAccountGift:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            DeleteBusinessAccountGift,
            ok=True,
            result=True,
        )

        response = await bot.delete_business_account_gift(business_connection_id="bc1", owned_gift_id="g1")
        bot.get_request()
        assert response == prepare_result.result
