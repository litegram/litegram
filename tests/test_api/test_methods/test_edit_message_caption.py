import datetime

import pytest

from litegram.methods import EditMessageCaption
from litegram.types import Chat, Message
from tests.mocked_bot import MockedBot


class TestEditMessageCaption:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditMessageCaption,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(),
                text="text",
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message | bool = await bot.edit_message_caption()
        bot.get_request()
        assert response == prepare_result.result
