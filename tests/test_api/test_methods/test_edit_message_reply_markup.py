from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditMessageReplyMarkup
from litegram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditMessageReplyMarkup:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(EditMessageReplyMarkup, ok=True, result=True)

        response: Message | bool = await bot.edit_message_reply_markup(
            chat_id=42,
            inline_message_id="inline message id",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="button", callback_data="placeholder")]]
            ),
        )
        bot.get_request()
        assert response == prepare_result.result
