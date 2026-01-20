from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.enums import StickerFormat
from litegram.methods import AddStickerToSet
from litegram.types import InputSticker

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestAddStickerToSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(AddStickerToSet, ok=True, result=True)

        response: bool = await bot.add_sticker_to_set(
            user_id=42,
            name="test stickers pack",
            sticker=InputSticker(sticker="file id", format=StickerFormat.STATIC, emoji_list=[":)"]),
        )
        bot.get_request()
        assert response == prepare_result.result
