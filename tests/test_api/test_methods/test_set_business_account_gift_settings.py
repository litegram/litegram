from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetBusinessAccountGiftSettings
from litegram.types import AcceptedGiftTypes

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetBusinessAccountGiftSettings:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetBusinessAccountGiftSettings, ok=True, result=True)

        response: bool = await bot.set_business_account_gift_settings(
            business_connection_id="test_connection_id",
            show_gift_button=True,
            accepted_gift_types=AcceptedGiftTypes(
                gifts_from_channels=True,
                unlimited_gifts=True,
                limited_gifts=True,
                unique_gifts=True,
                premium_subscription=True,
            ),
        )
        bot.get_request()
        assert response == prepare_result.result
