from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditStory
from litegram.types import Chat, InputStoryContentPhoto, Story

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditStory:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditStory,
            ok=True,
            result=Story(
                id=42,
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Story = await bot.edit_story(
            business_connection_id="test_connection_id",
            story_id=42,
            content=InputStoryContentPhoto(type="photo", photo="test_photo"),
            caption="Test caption",
        )
        bot.get_request()
        assert response == prepare_result.result
