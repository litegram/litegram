from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import BanChatSenderChat

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestBanChatSenderChat:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(BanChatSenderChat, ok=True, result=True)

        response: bool = await bot.ban_chat_sender_chat(
            chat_id=-42,
            sender_chat_id=-1337,
        )
        bot.get_request()
        assert response == prepare_result.result
