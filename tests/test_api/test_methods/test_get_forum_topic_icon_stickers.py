from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetForumTopicIconStickers

if TYPE_CHECKING:
    from litegram.types import Sticker
    from tests.mocked_bot import MockedBot


class TestGetForumTopicIconStickers:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetForumTopicIconStickers, ok=True, result=[])

        response: list[Sticker] = await bot.get_forum_topic_icon_stickers()
        bot.get_request()
        assert response == prepare_result.result
