from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import CloseForumTopic

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestCloseForumTopic:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(CloseForumTopic, ok=True, result=True)

        response: bool = await bot.close_forum_topic(
            chat_id=42,
            message_thread_id=42,
        )
        bot.get_request()
        assert response == prepare_result.result
