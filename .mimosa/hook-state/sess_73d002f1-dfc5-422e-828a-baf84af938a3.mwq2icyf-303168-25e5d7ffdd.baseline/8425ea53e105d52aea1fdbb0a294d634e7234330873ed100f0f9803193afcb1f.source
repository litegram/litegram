from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetBusinessConnection
from litegram.types import BusinessConnection, User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetBusinessConnection:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetBusinessConnection,
            ok=True,
            result=BusinessConnection(
                id="test",
                user=User(id=42, is_bot=False, first_name="User"),
                user_chat_id=42,
                date=42,
                can_reply=True,
                is_enabled=True,
            ),
        )
        response: BusinessConnection = await bot.get_business_connection(business_connection_id="test")
        bot.get_request()
        assert response == prepare_result.result
