import pytest

from litegram.methods import SetStickerEmojiList
from tests.mocked_bot import MockedBot


class TestSetStickerEmojiList:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetStickerEmojiList, ok=True, result=True)

        response: bool = await bot.set_sticker_emoji_list(sticker="sticker id", emoji_list=["X"])
        bot.get_request()
        assert response == prepare_result.result
