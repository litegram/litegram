from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteChatPhoto

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteChatPhoto:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeleteChatPhoto, ok=True, result=True)

        response: bool = await bot.delete_chat_photo(chat_id=42)
        bot.get_request()
        assert response == prepare_result.result
