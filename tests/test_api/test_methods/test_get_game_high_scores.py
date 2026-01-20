from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetGameHighScores
from litegram.types import GameHighScore, User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetGameHighScores:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetGameHighScores,
            ok=True,
            result=[GameHighScore(position=1, user=User(id=42, is_bot=False, first_name="User"), score=42)],
        )

        response: list[GameHighScore] = await bot.get_game_high_scores(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
