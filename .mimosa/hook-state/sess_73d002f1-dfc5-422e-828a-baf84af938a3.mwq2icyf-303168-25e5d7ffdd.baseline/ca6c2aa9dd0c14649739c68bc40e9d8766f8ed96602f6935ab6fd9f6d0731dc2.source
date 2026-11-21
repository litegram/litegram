from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import GetFile
from litegram.types import File

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetFile:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(GetFile, ok=True, result=File(file_id="file id", file_unique_id="file id"))

        response: File = await bot.get_file(file_id="file id")
        bot.get_request()
        assert response == prepare_result.result
