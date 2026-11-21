from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteChatStickerSet

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteChatStickerSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeleteChatStickerSet, ok=True, result=True)

        response: bool = await bot.delete_chat_sticker_set(chat_id=42)
        bot.get_request()
        assert response == prepare_result.result
