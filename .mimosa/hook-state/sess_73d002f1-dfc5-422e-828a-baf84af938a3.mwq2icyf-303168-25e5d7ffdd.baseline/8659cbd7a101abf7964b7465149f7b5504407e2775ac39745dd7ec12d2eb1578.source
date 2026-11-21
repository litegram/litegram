from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteStickerSet

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteStickerSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeleteStickerSet, ok=True, result=True)

        response: bool = await bot.delete_sticker_set(name="test")
        bot.get_request()
        assert response == prepare_result.result
