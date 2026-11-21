from __future__ import annotations

import datetime
import math
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
                location=Location(longitude=math.pi, latitude=math.pi),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_location(chat_id=42, latitude=math.pi, longitude=math.pi)
        bot.get_request()
        assert response == prepare_result.result
