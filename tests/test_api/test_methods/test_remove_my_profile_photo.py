"""Behavioral tests for removeMyProfilePhoto (Bot API 10.4)."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import RemoveMyProfilePhoto
from litegram.types import Chat, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestRemoveMyProfilePhoto:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            RemoveMyProfilePhoto,
            ok=True,
            result=True,
        )

        response = await bot.remove_my_profile_photo()
        bot.get_request()
        assert response == prepare_result.result
