from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import ApproveChatJoinRequest

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestApproveChatJoinRequest:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(ApproveChatJoinRequest, ok=True, result=None)

        response: bool = await bot.approve_chat_join_request(
            chat_id=-42,
            user_id=42,
        )
        bot.get_request()
        assert response == prepare_result.result
