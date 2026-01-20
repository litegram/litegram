from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import UnbanChatSenderChat

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestUnbanChatSenderChat:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(UnbanChatSenderChat, ok=True, result=True)

        response: bool = await bot.unban_chat_sender_chat(
            chat_id=-42,
            sender_chat_id=-1337,
        )
        bot.get_request()
        assert response == prepare_result.result
