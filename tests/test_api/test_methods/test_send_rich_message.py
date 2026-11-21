"""Behavioral tests for sendRichMessage (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendRichMessage
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendRichMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendRichMessage,
            ok=True,
            result=Message(
                message_id=42, date=datetime.datetime.now(datetime.UTC), chat=Chat(id=42, type="private"), text="test"
            ),
        )

        response = await bot.send_rich_message(rich_message={"blocks": [{"type": "paragraph", "text": "hello"}]})
        bot.get_request()
        assert response == prepare_result.result
