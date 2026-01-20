from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMyCommands

if TYPE_CHECKING:
    from litegram.types import BotCommand
    from tests.mocked_bot import MockedBot


class TestGetMyCommands:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetMyCommands, ok=True, result=None)

        response: list[BotCommand] = await bot.get_my_commands()
        bot.get_request()
        assert response == prepare_result.result
