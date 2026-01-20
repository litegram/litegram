from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import VerifyChat

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestVerifyChat:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(VerifyChat, ok=True, result=True)

        response: bool = await bot.verify_chat(chat_id=42)
        bot.get_request()
        assert response == prepare_result.result
