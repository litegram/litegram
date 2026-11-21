from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import RemoveUserVerification

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestRemoveUserVerification:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(RemoveUserVerification, ok=True, result=True)

        response: bool = await bot.remove_user_verification(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
