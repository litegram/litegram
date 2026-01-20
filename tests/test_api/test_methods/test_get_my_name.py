from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMyName
from litegram.types import BotName

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetMyName:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetMyName, ok=True, result=BotName(name="Test"))

        response: BotName = await bot.get_my_name()
        assert response == prepare_result.result
