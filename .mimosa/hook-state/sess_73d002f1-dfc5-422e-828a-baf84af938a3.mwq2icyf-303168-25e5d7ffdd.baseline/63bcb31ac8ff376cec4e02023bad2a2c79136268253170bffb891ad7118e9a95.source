"""Behavioral tests for sendRichMessageDraft (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendRichMessageDraft
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendRichMessageDraft:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendRichMessageDraft,
            ok=True,
            result=True,
        )

        response = await bot.send_rich_message_draft(chat_id=42, draft_id=42, rich_message={"blocks": [{"type": "paragraph", "text": "hello"}]})
        bot.get_request()
        assert response == prepare_result.result
