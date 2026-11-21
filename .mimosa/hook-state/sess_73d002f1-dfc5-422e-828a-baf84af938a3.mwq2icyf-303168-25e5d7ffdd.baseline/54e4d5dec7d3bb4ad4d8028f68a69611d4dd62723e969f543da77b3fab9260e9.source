from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetCustomEmojiStickerSetThumbnail

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetCustomEmojiStickerSetThumbnail:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetCustomEmojiStickerSetThumbnail, ok=True, result=True)

        response: bool = await bot.set_custom_emoji_sticker_set_thumbnail(name="test", custom_emoji_id="custom id")
        bot.get_request()
        assert response == prepare_result.result
