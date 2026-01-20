from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendLocation
from litegram.types import Chat, Location, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendLocation:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendLocation,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                location=Location(longitude=3.14, latitude=3.14),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_location(chat_id=42, latitude=3.14, longitude=3.14)
        bot.get_request()
        assert response == prepare_result.result
