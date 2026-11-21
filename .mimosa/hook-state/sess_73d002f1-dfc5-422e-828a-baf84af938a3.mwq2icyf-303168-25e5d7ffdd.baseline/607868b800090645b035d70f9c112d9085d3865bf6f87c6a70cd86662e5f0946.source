from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditChatInviteLink
from litegram.types import ChatInviteLink, User

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditChatInviteLink:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditChatInviteLink,
            ok=True,
            result=ChatInviteLink(
                invite_link="https://t.me/username2",
                creator=User(id=42, is_bot=False, first_name="User"),
                is_primary=False,
                is_revoked=False,
                creates_join_request=False,
            ),
        )

        response: ChatInviteLink = await bot.edit_chat_invite_link(
            chat_id=-42, invite_link="https://t.me/username", member_limit=1
        )
        bot.get_request()
        assert response == prepare_result.result
