from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.enums import StickerFormat
from litegram.methods import UploadStickerFile
from litegram.types import BufferedInputFile, File

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestUploadStickerFile:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            UploadStickerFile, ok=True, result=File(file_id="file id", file_unique_id="file id")
        )

        response: File = await bot.upload_sticker_file(
            user_id=42,
            sticker=BufferedInputFile(b"", "file.png"),
            sticker_format=StickerFormat.STATIC,
        )
        bot.get_request()
        assert response == prepare_result.result
