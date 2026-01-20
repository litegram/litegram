from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendContact
from litegram.types import Chat, Contact, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendContact:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendContact,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                contact=Contact(phone_number="911", first_name="911"),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_contact(chat_id=42, phone_number="911", first_name="911")
        bot.get_request()
        assert response == prepare_result.result
