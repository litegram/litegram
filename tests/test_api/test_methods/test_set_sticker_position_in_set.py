from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetStickerPositionInSet

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetStickerPositionInSet:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetStickerPositionInSet, ok=True, result=True)

        response: bool = await bot.set_sticker_position_in_set(sticker="sticker", position=42)
        bot.get_request()
        assert response == prepare_result.result
