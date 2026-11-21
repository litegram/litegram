from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendMessageDraft

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendMessageDraft:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendMessageDraft,
            ok=True,
            result=True,
        )

        response: bool = await bot.send_message_draft(
            chat_id=42,
            draft_id=1,
            text="test draft",
        )
        bot.get_request()
        assert response == prepare_result.result
