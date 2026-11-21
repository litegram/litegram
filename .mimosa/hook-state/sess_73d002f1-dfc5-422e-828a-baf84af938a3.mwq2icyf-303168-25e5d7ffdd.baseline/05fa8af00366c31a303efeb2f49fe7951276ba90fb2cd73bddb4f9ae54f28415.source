from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetStickerSet
from litegram.types import Sticker, StickerSet

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetStickerSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetStickerSet,
            ok=True,
            result=StickerSet(
                name="test",
                title="test",
                is_animated=False,
                is_video=False,
                stickers=[
                    Sticker(
                        file_id="file if",
                        width=42,
                        height=42,
                        is_animated=False,
                        is_video=False,
                        file_unique_id="file id",
                        type="regular",
                    )
                ],
                sticker_type="regular",
            ),
        )

        response: StickerSet = await bot.get_sticker_set(name="test")
        bot.get_request()
        assert response == prepare_result.result
