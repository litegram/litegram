from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetUserGifts
from litegram.types import Gift, OwnedGiftRegular, OwnedGifts, Sticker

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetUserGifts:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetUserGifts,
            ok=True,
            result=OwnedGifts(
                total_count=1,
                gifts=[
                    OwnedGiftRegular(
                        gift=Gift(
                            id="test_gift_id",
                            sticker=Sticker(
                                file_id="test_file_id",
                                file_unique_id="test_file_unique_id",
                                type="regular",
                                width=512,
                                height=512,
                                is_animated=False,
                                is_video=False,
                            ),
                            star_count=100,
                        ),
                        send_date=int(datetime.datetime.now(datetime.UTC).timestamp()),
                    )
                ],
            ),
        )

        response: OwnedGifts = await bot.get_user_gifts(
            user_id=42,
            limit=10,
        )
        bot.get_request()
        assert response == prepare_result.result
