from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

import pytest

from litegram.methods import CopyMessages
from litegram.types import MessageId

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestCopyMessages:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            CopyMessages,
            ok=True,
            result=[
                MessageId(message_id=randint(100, 200)),
                MessageId(message_id=randint(300, 400)),
            ],
        )

        response: list[MessageId] = await bot.copy_messages(
            chat_id=randint(1000, 9999),
            from_chat_id=randint(1000, 9999),
            message_ids=[
                randint(1000, 4999),
                randint(5000, 9999),
            ],
        )
        request = bot.get_request()
        assert request
        assert response == prepare_result.result
