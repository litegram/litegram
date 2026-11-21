"""Behavioral tests for savePreparedKeyboardButton (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SavePreparedKeyboardButton
from litegram.types import Chat, Message, PreparedKeyboardButton

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSavePreparedKeyboardButton:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SavePreparedKeyboardButton,
            ok=True,
            result=PreparedKeyboardButton(id="k1", text="btn"),
        )

        response = await bot.save_prepared_keyboard_button(user_id=42, button={"text": "btn"})
        bot.get_request()
        assert response == prepare_result.result
