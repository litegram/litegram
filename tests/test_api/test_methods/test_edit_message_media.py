import pytest

from litegram.methods import EditMessageMedia
from litegram.types import BufferedInputFile, InputMediaPhoto, Message
from tests.mocked_bot import MockedBot


class TestEditMessageMedia:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(EditMessageMedia, ok=True, result=True)

        response: Message | bool = await bot.edit_message_media(
            media=InputMediaPhoto(media=BufferedInputFile(b"", "photo.png"))
        )
        bot.get_request()
        assert response == prepare_result.result
