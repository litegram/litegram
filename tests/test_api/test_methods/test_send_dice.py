from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendDice
from tests.mocked_bot import MockedBot

if TYPE_CHECKING:
    from litegram.types import Message


class TestSendDice:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SendDice, ok=True, result=None)

        response: Message = await bot.send_dice(chat_id=42)
        bot.get_request()
        assert response == prepare_result.result
