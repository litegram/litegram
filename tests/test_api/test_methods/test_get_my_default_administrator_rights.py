from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetMyDefaultAdministratorRights
from litegram.types import ChatAdministratorRights

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetMyDefaultAdministratorRights:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetMyDefaultAdministratorRights,
            ok=True,
            result=ChatAdministratorRights(
                is_anonymous=False,
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_post_stories=False,
                can_edit_stories=False,
                can_delete_stories=False,
            ),
        )

        response: ChatAdministratorRights = await bot.get_my_default_administrator_rights()
        bot.get_request()
        assert response == prepare_result.result
