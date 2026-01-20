from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import EditMessageChecklist
from litegram.types import Chat, InputChecklist, InputChecklistTask, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestEditMessageChecklist:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            EditMessageChecklist,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                chat=Chat(id=42, type="private"),
            ),
        )

        checklist = InputChecklist(
            title="Updated Checklist",
            tasks=[
                InputChecklistTask(id=1, text="Updated Task 1"),
                InputChecklistTask(id=2, text="Updated Task 2"),
            ],
        )

        response: Message = await bot.edit_message_checklist(
            business_connection_id="test_connection",
            chat_id=42,
            message_id=42,
            checklist=checklist,
        )
        bot.get_request()
        assert response == prepare_result.result
