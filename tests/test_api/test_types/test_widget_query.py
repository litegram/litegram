"""Tests for the Widget/WidgetQuery family introduced in Bot API 10.4."""

from __future__ import annotations

import pytest

from litegram.enums import WidgetQueryTypeType
from litegram.types import (
    User,
    WidgetQuery,
    WidgetQueryTypeData,
    WidgetQueryTypeSentTransaction,
    WidgetQueryTypeSignData,
)


class TestWidgetQueryType:
    @pytest.mark.parametrize(
        "raw_type, expected_cls, expected_value, extra",
        [
            ("data", WidgetQueryTypeData, "data", {}),
            (
                "sign_data",
                WidgetQueryTypeSignData,
                "sign_data",
                {"wallet": {"address": "addr", "amount": "1"}, "sign_data": "signed"},
            ),
            (
                "sent_transaction",
                WidgetQueryTypeSentTransaction,
                "sent_transaction",
                {"wallet": {"address": "addr", "amount": "1"}, "msg_hash": "hash"},
            ),
        ],
    )
    def test_discriminated_union(self, raw_type, expected_cls, expected_value, extra):
        query = WidgetQuery.model_validate(
            {
                "id": "q1",
                "from": {"id": 42, "is_bot": False, "first_name": "Test"},
                "chat_instance": "inst",
                "type": {"type": raw_type, **extra},
                "data": "payload",
            }
        )
        assert isinstance(query.type, expected_cls)
        assert query.type.type == expected_value

    def test_enum_values(self):
        assert WidgetQueryTypeType.DATA == "data"
        assert WidgetQueryTypeType.SIGN_DATA == "sign_data"
        assert WidgetQueryTypeType.SENT_TRANSACTION == "sent_transaction"
