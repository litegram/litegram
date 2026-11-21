from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import PinChatMessage

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestPinChatMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(PinChatMessage, ok=True, result=True)

        response: bool = await bot.pin_chat_message(chat_id=-42, message_id=42)
        bot.get_request()
        assert response == prepare_result.result
