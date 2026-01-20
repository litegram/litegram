from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SavePreparedInlineMessage
from litegram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    PreparedInlineMessage,
)

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSavePreparedInlineMessage:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SavePreparedInlineMessage,
            ok=True,
            result=PreparedInlineMessage(
                id="id",
                expiration_date=datetime.now(UTC) + timedelta(days=1),
            ),
        )

        response: PreparedInlineMessage = await bot.save_prepared_inline_message(
            user_id=42,
            result=InlineQueryResultArticle(
                id="id",
                title="title",
                input_message_content=InputTextMessageContent(
                    message_text="message_text",
                ),
            ),
        )
        bot.get_request()
        assert response == prepare_result.result
