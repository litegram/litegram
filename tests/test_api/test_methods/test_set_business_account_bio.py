from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetBusinessAccountBio

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetBusinessAccountBio:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetBusinessAccountBio, ok=True, result=True)

        response: bool = await bot.set_business_account_bio(
            business_connection_id="test_connection_id",
            bio="This is a test bio for the business account",
        )
        bot.get_request()
        assert response == prepare_result.result
