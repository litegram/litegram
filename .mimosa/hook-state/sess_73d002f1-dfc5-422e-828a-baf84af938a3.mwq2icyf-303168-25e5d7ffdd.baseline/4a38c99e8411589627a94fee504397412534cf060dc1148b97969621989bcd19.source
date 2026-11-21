from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetBusinessAccountProfilePhoto
from litegram.types import InputProfilePhotoStatic

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetBusinessAccountProfilePhoto:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetBusinessAccountProfilePhoto, ok=True, result=True)

        response: bool = await bot.set_business_account_profile_photo(
            business_connection_id="test_connection_id",
            photo=InputProfilePhotoStatic(photo="test_photo_file_id"),
            is_public=True,
        )
        bot.get_request()
        assert response == prepare_result.result
