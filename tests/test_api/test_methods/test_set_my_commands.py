from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetMyCommands

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetMyCommands:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetMyCommands, ok=True, result=None)

        response: bool = await bot.set_my_commands(
            commands=[],
        )
        bot.get_request()
        assert response == prepare_result.result
