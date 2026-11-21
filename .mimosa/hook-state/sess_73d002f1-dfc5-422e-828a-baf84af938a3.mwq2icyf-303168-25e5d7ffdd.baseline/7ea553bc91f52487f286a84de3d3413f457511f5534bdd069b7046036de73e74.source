from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendPaidMedia
from litegram.types import (
    Chat,
    InputPaidMediaPhoto,
    Message,
    PaidMediaInfo,
    PaidMediaPhoto,
    PhotoSize,
)

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendPaidMedia:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendPaidMedia,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                chat=Chat(id=42, type="private"),
                paid_media=PaidMediaInfo(
                    paid_media=[PaidMediaPhoto(photo=[PhotoSize(file_id="test", width=42, height=42, file_unique_id="test")])],
                    star_count=1,
                ),
            ),
        )

        response: Message = await bot.send_paid_media(chat_id=-42, star_count=1, media=[InputPaidMediaPhoto(media="file_id")])
        bot.get_request()
        assert response == prepare_result.result
