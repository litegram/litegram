from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import RepostStory
from litegram.types import Chat, Story

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestRepostStory:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            RepostStory,
            ok=True,
            result=Story(
                id=42,
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Story = await bot.repost_story(
            business_connection_id="test_connection_id",
            from_chat_id=123,
            from_story_id=456,
            active_period=6 * 3600,
        )
        bot.get_request()
        assert response == prepare_result.result
