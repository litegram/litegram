from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetAvailableGifts
from litegram.types import Gift, Gifts, Sticker

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetAvailableGifts:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetAvailableGifts,
            ok=True,
            result=Gifts(
                gifts=[
                    Gift(
                        id="gift_id",
                        sticker=Sticker(
                            file_id="file_id",
                            file_unique_id="file_id",
                            type="regular",
                            width=512,
                            height=512,
                            is_animated=False,
                            is_video=False,
                        ),
                        star_count=1,
                    )
                ]
            ),
        )

        response: Gifts = await bot.get_available_gifts()
        bot.get_request()
        assert response == prepare_result.result
