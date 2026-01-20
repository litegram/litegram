from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import DeleteBusinessMessages

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestDeleteBusinessMessages:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(DeleteBusinessMessages, ok=True, result=True)

        response: bool = await bot.delete_business_messages(business_connection_id="test_connection_id", message_ids=[1, 2, 3])
        bot.get_request()
        assert response == prepare_result.result
