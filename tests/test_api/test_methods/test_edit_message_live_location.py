from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditMessageLiveLocation

if TYPE_CHECKING:
    from litegram.types import Message
    from tests.mocked_bot import MockedBot


class TestEditMessageLiveLocation:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(EditMessageLiveLocation, ok=True, result=True)

        response: Message | bool = await bot.edit_message_live_location(latitude=3.141592, longitude=3.141592)
        bot.get_request()
        assert response == prepare_result.result
