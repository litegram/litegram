from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetMyName

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetMyName:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetMyName, ok=True, result=True)

        response: bool = await bot.set_my_name()
        assert response == prepare_result.result
