from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteMessages

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteMessages:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            DeleteMessages,
            ok=True,
            result=True,
        )

        response: bool = await bot.delete_messages(
            chat_id=42,
            message_ids=[13, 77],
        )
        request = bot.get_request()
        assert request
        assert response == prepare_result.result
