from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetChatStickerSet

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetChatStickerSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetChatStickerSet, ok=True, result=True)

        response: bool = await bot.set_chat_sticker_set(chat_id=-42, sticker_set_name="test")
        bot.get_request()
        assert response == prepare_result.result
