from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetGameScore

if TYPE_CHECKING:
    from litegram.types import Message
    from tests.mocked_bot import MockedBot


class TestSetGameScore:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetGameScore, ok=True, result=True)

        response: Message | bool = await bot.set_game_score(user_id=42, score=100500, inline_message_id="inline message")
        bot.get_request()
        assert response == prepare_result.result
