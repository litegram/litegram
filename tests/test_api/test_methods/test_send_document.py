from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendDocument
from litegram.types import Chat, Document, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendDocument:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendDocument,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                document=Document(file_id="file id", file_unique_id="file id"),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_document(chat_id=42, document="file id")
        bot.get_request()
        assert response == prepare_result.result
