from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendVideoNote
from litegram.types import BufferedInputFile, Chat, Message, VideoNote

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendVideoNote:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendVideoNote,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                video_note=VideoNote(file_id="file id", length=0, duration=0, file_unique_id="file id"),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_video_note(
            chat_id=42,
            video_note="file id",
            thumbnail=BufferedInputFile(b"", "file.png"),
        )
        bot.get_request()
        assert response == prepare_result.result
