from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import StopMessageLiveLocation

if TYPE_CHECKING:
    from litegram.types import Message
    from tests.mocked_bot import MockedBot


class TestStopMessageLiveLocation:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(StopMessageLiveLocation, ok=True, result=True)

        response: Message | bool = await bot.stop_message_live_location(inline_message_id="inline message id")
        bot.get_request()
        assert response == prepare_result.result
