from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import pytest

from litegram.methods import SendInvoice
from litegram.types import Chat, Invoice, LabeledPrice, Message

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestSendInvoice:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(
            SendInvoice,
            ok=True,
            result=Message(
                message_id=42,
                date=datetime.datetime.now(datetime.UTC),
                invoice=Invoice(
                    title="test",
                    description="test",
                    start_parameter="brilliant",
                    currency="BTC",
                    total_amount=1,
                ),
                chat=Chat(id=42, type="private"),
            ),
        )

        response: Message = await bot.send_invoice(
            chat_id=42,
            title="test",
            description="test",
            payload="payload",
            provider_token="TEST:token",
            start_parameter="brilliant",
            currency="BTC",
            prices=[LabeledPrice(amount=1, label="test")],
        )
        bot.get_request()
        assert response == prepare_result.result
