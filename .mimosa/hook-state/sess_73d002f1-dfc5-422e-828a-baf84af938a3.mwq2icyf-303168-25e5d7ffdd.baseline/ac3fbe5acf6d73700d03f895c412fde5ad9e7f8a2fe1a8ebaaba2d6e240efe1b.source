from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.enums import ChatAction
from litegram.methods import SendChatAction

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendChatAction:
    @pytest.mark.anyio
    async def test_chat_action_class(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SendChatAction, ok=True, result=True)

        response: bool = await bot.send_chat_action(chat_id=42, action=ChatAction.TYPING)
        bot.get_request()
        assert response == prepare_result.result
