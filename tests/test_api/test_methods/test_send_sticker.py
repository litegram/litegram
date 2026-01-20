from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendSticker
from litegram.types import Chat, Message, Sticker

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendSticker:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendSticker,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                sticker=Sticker(
                    file_id="file id",
                    width=42,
                    height=42,
                    is_animated=False,
                    is_video=False,
                    file_unique_id="file id",
                    type="regular",
                ),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_sticker(chat_id=42, sticker="file id")
        bot.get_request()
        assert response == prepare_result.result
