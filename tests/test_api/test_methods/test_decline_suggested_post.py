from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeclineSuggestedPost

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeclineSuggestedPost:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeclineSuggestedPost, ok=True, result=True)

        response: bool = await bot.decline_suggested_post(
            chat_id=-42,
            message_id=42,
        )
        bot.get_request()
        assert response == prepare_result.result
