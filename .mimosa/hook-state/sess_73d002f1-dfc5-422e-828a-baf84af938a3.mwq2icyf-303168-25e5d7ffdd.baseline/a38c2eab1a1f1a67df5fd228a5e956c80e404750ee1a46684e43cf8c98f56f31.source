from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetMyDefaultAdministratorRights

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetMyDefaultAdministratorRights:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetMyDefaultAdministratorRights, ok=True, result=True)

        response: bool = await bot.set_my_default_administrator_rights()
        bot.get_request()
        assert response == prepare_result.result
