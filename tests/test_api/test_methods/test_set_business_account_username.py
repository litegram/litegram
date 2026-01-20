from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetBusinessAccountUsername

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetBusinessAccountUsername:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetBusinessAccountUsername, ok=True, result=True)

        response: bool = await bot.set_business_account_username(
            business_connection_id="test_connection_id", username="test_business_username"
        )
        bot.get_request()
        assert response == prepare_result.result
