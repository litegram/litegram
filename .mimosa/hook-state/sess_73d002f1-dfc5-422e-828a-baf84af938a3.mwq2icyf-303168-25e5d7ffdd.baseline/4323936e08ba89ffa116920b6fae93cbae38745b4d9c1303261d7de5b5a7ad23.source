"""Behavioral tests for getUniqueGift (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetUniqueGift
from litegram.types import Chat, Message, UniqueGift

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetUniqueGift:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetUniqueGift,
            ok=True,
            result=UniqueGift(gift_id="g1", base_name="base", name="gift", number=1, model={"name": "m", "sticker": {"file_id": "f", "file_unique_id": "fu", "type": "regular", "width": 512, "height": 512, "is_animated": False, "is_video": False}, "rarity_per_mille": 1}, symbol={"name": "s", "sticker": {"file_id": "f", "file_unique_id": "fu", "type": "regular", "width": 512, "height": 512, "is_animated": False, "is_video": False}, "rarity_per_mille": 1}, backdrop={"name": "b", "colors": {"center_color": 0, "edge_color": 0, "symbol_color": 0, "text_color": 0}, "rarity_per_mille": 1}),
        )

        response = await bot.get_unique_gift(name="gift")
        bot.get_request()
        assert response == prepare_result.result
