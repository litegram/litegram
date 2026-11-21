from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMe
from litegram.types import User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetMe:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetMe, ok=True, result=User(id=42, is_bot=False, first_name="User"))
        response: User = await bot.get_me()
        bot.get_request()
        assert response == prepare_result.result

    @pytest.mark.anyio
    async def test_me_property(self, bot: MockedBot):
        response: User = await bot.me()
        assert isinstance(response, User)
        assert response == bot._me
