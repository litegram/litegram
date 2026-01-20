from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest

from litegram.enums import TransactionPartnerUserTransactionTypeEnum
from litegram.methods import GetStarTransactions
from litegram.types import (
    StarTransaction,
    StarTransactions,
    TransactionPartnerUser,
    User,
)

if TYPE_CHECKING:
    from tests.mocked_bot import MockedBot


class TestGetStarTransactions:
    @pytest.mark.anyio
    async def test_bot_method(self, bot: MockedBot):
        user = User(id=42, is_bot=False, first_name="Test")
        prepare_result = bot.add_result_for(
            GetStarTransactions,
            ok=True,
            result=StarTransactions(
                transactions=[
                    StarTransaction(
                        id="test1",
                        user=user,
                        amount=1,
                        date=datetime.now(UTC),
                        source=TransactionPartnerUser(
                            user=user,
                            transaction_type=TransactionPartnerUserTransactionTypeEnum.GIFT_PURCHASE,
                        ),
                    ),
                    StarTransaction(
                        id="test2",
                        user=user,
                        amount=1,
                        date=datetime.now(UTC),
                        receiver=TransactionPartnerUser(
                            user=user,
                            transaction_type=TransactionPartnerUserTransactionTypeEnum.GIFT_PURCHASE,
                        ),
                    ),
                ]
            ),
        )

        response: StarTransactions = await bot.get_star_transactions(limit=10, offset=0)
        bot.get_request()
        assert response == prepare_result.result
