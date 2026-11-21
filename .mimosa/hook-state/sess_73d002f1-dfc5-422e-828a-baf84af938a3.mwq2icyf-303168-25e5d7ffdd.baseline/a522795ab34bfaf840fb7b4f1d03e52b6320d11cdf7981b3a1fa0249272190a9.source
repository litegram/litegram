from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMyShortDescription
from litegram.types import BotShortDescription

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetMyShortDescription:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetMyShortDescription, ok=True, result=BotShortDescription(short_description="Test")
        )

        response: BotShortDescription = await bot.get_my_short_description()
        bot.get_request()
        assert response == prepare_result.result
