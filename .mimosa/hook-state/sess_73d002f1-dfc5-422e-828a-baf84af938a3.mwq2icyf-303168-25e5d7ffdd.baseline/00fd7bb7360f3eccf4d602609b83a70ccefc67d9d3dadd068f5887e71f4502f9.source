from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteStory

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteStory:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeleteStory, ok=True, result=True)

        response: bool = await bot.delete_story(business_connection_id="test_connection_id", story_id=42)
        bot.get_request()
        assert response == prepare_result.result
