from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendAudio
from litegram.types import Audio, Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendAudio:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendAudio,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                audio=Audio(file_id="file id", duration=42, file_unique_id="file id"),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_audio(chat_id=42, audio="file id")
        bot.get_request()
        assert response == prepare_result.result
