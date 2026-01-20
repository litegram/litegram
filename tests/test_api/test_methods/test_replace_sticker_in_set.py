from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import ReplaceStickerInSet
from litegram.types import InputSticker

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestReplaceStickerInSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(ReplaceStickerInSet, ok=True, result=True)

        response: bool = await bot.replace_sticker_in_set(
            user_id=42,
            name="test",
            old_sticker="test",
            sticker=InputSticker(
                sticker="test",
                format="static",
                emoji_list=["test"],
            ),
        )
        bot.get_request()
        assert response == prepare_result.result
