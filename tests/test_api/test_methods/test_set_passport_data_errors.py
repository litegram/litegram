from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import SetPassportDataErrors
from litegram.types import PassportElementErrorFile

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSetPassportDataErrors:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(SetPassportDataErrors, ok=True, result=True)

        response: bool = await bot.set_passport_data_errors(
            user_id=42,
            errors=[
                PassportElementErrorFile(
                    type="type",
                    file_hash="hash",
                    message="message",
                )
            ],
        )
        bot.get_request()
        assert response == prepare_result.result
