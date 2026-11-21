from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMyStarBalance
from litegram.types import StarAmount

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetMyStarBalance:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetMyStarBalance,
            ok=True,
            result=StarAmount(
                amount=100,
            ),
        )

        response: StarAmount = await bot.get_my_star_balance()
        bot.get_request()
        assert response == prepare_result.result
