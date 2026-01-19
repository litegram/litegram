import pytest

from litegram.methods import CopyMessage
from litegram.types import MessageId
from tests.mocked_bot import MockedBot


class TestCopyMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(CopyMessage, ok=True, result=MessageId(message_id=42))

        response: MessageId = await bot.copy_message(
            chat_id=42,
            from_chat_id=42,
            message_id=42,
        )
        bot.get_request()
        assert response == prepare_result.result
