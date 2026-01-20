from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetChat
from litegram.types import AcceptedGiftTypes, ChatFullInfo

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetChat:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            GetChat,
            ok=True,
            result=ChatFullInfo(
                id=-42,
                type="channel",
                title="chat",
                accent_color_id=0,
                max_reaction_count=0,
                accepted_gift_types=AcceptedGiftTypes(
                    unlimited_gifts=True,
                    limited_gifts=True,
                    unique_gifts=True,
                    premium_subscription=True,
                    gifts_from_channels=True,
                ),
            ),
        )

        response: ChatFullInfo = await bot.get_chat(chat_id=-42)
        bot.get_request()
        assert response == prepare_result.result
