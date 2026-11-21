from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMyDescription
from litegram.types import BotDescription

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetMyDescription:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetMyDescription, ok=True, result=BotDescription(description="Test"))

        response: BotDescription = await bot.get_my_description()
        bot.get_request()
        assert response == prepare_result.result
