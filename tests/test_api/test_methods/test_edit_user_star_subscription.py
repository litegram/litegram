from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditUserStarSubscription

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditUserStarSubscription:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(EditUserStarSubscription, ok=True, result=True)

        response: bool = await bot.edit_user_star_subscription(
            user_id=42,
            telegram_payment_charge_id="telegram_payment_charge_id",
            is_canceled=False,
        )
        bot.get_request()
        assert response == prepare_result.result
