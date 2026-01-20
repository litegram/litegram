from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import RefundStarPayment

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestRefundStarPayment:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(RefundStarPayment, ok=True, result=True)

        response: bool = await bot.refund_star_payment(
            user_id=42,
            telegram_payment_charge_id="12345",
        )
        bot.get_request()
        assert response == prepare_result.result
