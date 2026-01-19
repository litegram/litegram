import pytest

from litegram.methods import SetStickerMaskPosition
from tests.mocked_bot import MockedBot


class TestSetStickerEmojiList:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetStickerMaskPosition, ok=True, result=True)

        response: bool = await bot.set_sticker_mask_position(sticker="sticker id")
        bot.get_request()
        assert response == prepare_result.result
