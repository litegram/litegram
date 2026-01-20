from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from litegram.methods import CreateInvoiceLink
from litegram.types import LabeledPrice

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestCreateInvoiceLink:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        prepare_result = bot.add_result_for(CreateInvoiceLink, ok=True, result="https://t.me/invoice/example")

        response: str = await bot.create_invoice_link(
            title="test",
            description="test",
            payload="test",
            provider_token="test",
            currency="BTC",
            prices=[LabeledPrice(label="Test", amount=1)],
        )
        bot.get_request()
        assert response == prepare_result.result
