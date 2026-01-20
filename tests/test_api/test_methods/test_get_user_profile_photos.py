from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetUserProfilePhotos
from litegram.types import PhotoSize, UserProfilePhotos

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetUserProfilePhotos:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetUserProfilePhotos,
            ok=True,
            result=UserProfilePhotos(
                total_count=1,
                photos=[[PhotoSize(file_id="file_id", width=42, height=42, file_unique_id="file id")]],
            ),
        )

        response: UserProfilePhotos = await bot.get_user_profile_photos(user_id=42)
        bot.get_request()
        assert response == prepare_result.result
