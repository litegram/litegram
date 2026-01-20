from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import ConvertGiftToStars

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestConvertGiftToStars:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(ConvertGiftToStars, ok=True, result=True)

        response: bool = await bot.convert_gift_to_stars(
            business_connection_id="test_connection_id", owned_gift_id="test_gift_id"
        )
        bot.get_request()
        assert response == prepare_result.result
