from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import AnswerShippingQuery

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestAnswerShippingQuery:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(AnswerShippingQuery, ok=True, result=True)

        response: bool = await bot.answer_shipping_query(shipping_query_id="query id", ok=True)
        bot.get_request()
        assert response == prepare_result.result
