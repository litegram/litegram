from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import ReopenForumTopic

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestReopenForumTopic:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(ReopenForumTopic, ok=True, result=None)

        response: bool = await bot.reopen_forum_topic(
            chat_id=42,
            message_thread_id=42,
        )
        bot.get_request()
        assert response == prepare_result.result
