"""Behavioral tests for setMyProfilePhoto (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetMyProfilePhoto
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetMyProfilePhoto:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SetMyProfilePhoto,
            ok=True,
            result=True,
        )

        response = await bot.set_my_profile_photo(photo={"type": "static", "photo": "photo-id"})
        bot.get_request()
        assert response == prepare_result.result
