from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import ApproveSuggestedPost

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestApproveSuggestedPost:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(ApproveSuggestedPost, ok=True, result=True)

        response: bool = await bot.approve_suggested_post(
            chat_id=-42,
            message_id=42,
        )
        bot.get_request()
        assert response == prepare_result.result
