from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetChatMemberCount

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetChatMembersCount:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetChatMemberCount, ok=True, result=42)

        response: int = await bot.get_chat_member_count(chat_id=-42)
        bot.get_request()
        assert response == prepare_result.result
