from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetChatPermissions
from litegram.types import ChatPermissions

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetChatPermissions:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetChatPermissions, ok=True, result=True)

        response: bool = await bot.set_chat_permissions(chat_id=-42, permissions=ChatPermissions(can_send_messages=False))
        bot.get_request()
        assert response == prepare_result.result
