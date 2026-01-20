from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendGift

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendGift:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SendGift, ok=True, result=True)

        response: bool = await bot.send_gift(user_id=42, gift_id="gift_id")
        bot.get_request()
        assert response == prepare_result.result
