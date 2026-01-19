import pytest

from litegram.methods import SetStickerKeywords
from tests.mocked_bot import MockedBot


class TestSetStickerKeywords:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetStickerKeywords, ok=True, result=True)

        response: bool = await bot.set_sticker_keywords(sticker="sticker id", keywords=["X"])
        bot.get_request()
        assert response == prepare_result.result
