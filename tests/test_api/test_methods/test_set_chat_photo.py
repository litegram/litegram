from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetChatPhoto
from litegram.types import BufferedInputFile

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetChatPhoto:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetChatPhoto, ok=True, result=True)

        response: bool = await bot.set_chat_photo(chat_id=-42, photo=BufferedInputFile(b"", filename="file.png"))
        bot.get_request()
        assert response == prepare_result.result
