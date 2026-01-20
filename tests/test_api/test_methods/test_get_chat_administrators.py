from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetChatAdministrators
from litegram.types import ChatMember, ChatMemberOwner, User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetChatAdministrators:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetChatAdministrators,
            ok=True,
            result=[ChatMemberOwner(user=User(id=42, is_bot=False, first_name="User"), is_anonymous=False)],
        )
        response: list[ChatMember] = await bot.get_chat_administrators(chat_id=-42)
        bot.get_request()
        assert response == prepare_result.result
