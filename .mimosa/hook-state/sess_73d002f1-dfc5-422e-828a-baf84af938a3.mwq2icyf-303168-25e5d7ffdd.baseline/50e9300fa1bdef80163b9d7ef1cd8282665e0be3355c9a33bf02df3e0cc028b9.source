from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import CreateForumTopic
from litegram.types import ForumTopic

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestCreateForumTopic:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            CreateForumTopic,
            ok=True,
            result=ForumTopic(message_thread_id=42, name="test", icon_color=0xFFD67E),
        )

        response: ForumTopic = await bot.create_forum_topic(
            chat_id=42,
            name="test",
        )
        bot.get_request()
        assert response == prepare_result.result
