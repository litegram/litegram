from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import UnbanChatMember

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestUnbanChatMember:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(UnbanChatMember, ok=True, result=True)

        response: bool = await bot.unban_chat_member(chat_id=-42, user_id=42)
        bot.get_request()
        assert response == prepare_result.result
