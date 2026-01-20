from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import AnswerInlineQuery
from litegram.types import InlineQueryResultArticle, InputTextMessageContent

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestAnswerInlineQuery:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(AnswerInlineQuery, ok=True, result=True)

        response: bool = await bot.answer_inline_query(
            inline_query_id="query id",
            results=[
                InlineQueryResultArticle(
                    id="1",
                    title="title",
                    input_message_content=InputTextMessageContent(message_text="text"),
                )
            ],
        )
        bot.get_request()
        assert response == prepare_result.result
