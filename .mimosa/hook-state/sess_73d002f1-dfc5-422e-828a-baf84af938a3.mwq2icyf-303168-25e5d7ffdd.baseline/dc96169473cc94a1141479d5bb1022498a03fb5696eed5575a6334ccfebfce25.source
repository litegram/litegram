from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.enums import StickerFormat
from litegram.methods import CreateNewStickerSet
from litegram.types import FSInputFile, InputSticker

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestCreateNewStickerSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(CreateNewStickerSet, ok=True, result=True)

        response: bool = await bot.create_new_sticker_set(
            user_id=42,
            name="name",
            title="title",
            stickers=[
                InputSticker(sticker="file id", format=StickerFormat.STATIC, emoji_list=[":)"]),
                InputSticker(sticker=FSInputFile("file.png"), format=StickerFormat.STATIC, emoji_list=["=("]),
            ],
            sticker_format=StickerFormat.STATIC,
        )
        bot.get_request()
        assert response == prepare_result.result
