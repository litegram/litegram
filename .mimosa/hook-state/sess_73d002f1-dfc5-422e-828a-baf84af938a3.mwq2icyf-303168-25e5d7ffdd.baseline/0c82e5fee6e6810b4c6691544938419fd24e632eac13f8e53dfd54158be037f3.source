from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import PostStory
from litegram.types import Chat, InputStoryContentPhoto, Story

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestPostStory:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            PostStory,
            ok=True,
            result=Story(
                id=42,
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Story = await bot.post_story(
            business_connection_id="test_connection_id",
            content=InputStoryContentPhoto(type="photo", photo="test_photo"),
            active_period=6 * 3600,  # 6 hours
            caption="Test story caption",
        )
        bot.get_request()
        assert response == prepare_result.result
