from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetMyDescription

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetMyDescription:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetMyDescription, ok=True, result=True)

        response: bool = await bot.set_my_description(description="Test")
        bot.get_request()
        assert response == prepare_result.result
