from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditMessageText

if TYPE_CHECKING:
    from litegram.types import Message
    from tests.mocked_bot import MockedBot


class TestEditMessageText:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(EditMessageText, ok=True, result=True)

        response: Message | bool = await bot.edit_message_text(chat_id=42, inline_message_id="inline message id", text="text")
        bot.get_request()
        assert response == prepare_result.result
