"""Regression tests for the ``purchased_paid_media`` field name fix.

The legacy code named the field ``paid_media_purchased`` while the Bot API
page uses ``purchased_paid_media`` — the field would never deserialize from
real Telegram payloads. Bot API 10.4 keeps ``purchased_paid_media``.
"""

from __future__ import annotations

from litegram.types import PaidMediaPurchased, Update


class TestPurchasedPaidMedia:
    def test_update_deserializes_real_payload(self):
        update = Update.model_validate(
            {
                "update_id": 42,
                "purchased_paid_media": {
                    "from": {"id": 42, "is_bot": False, "first_name": "Test"},
                    "paid_media_payload": "payload",
                },
            }
        )
        assert update.purchased_paid_media is not None
        assert isinstance(update.purchased_paid_media, PaidMediaPurchased)
        assert update.purchased_paid_media.from_user.id == 42

    def test_event_type(self):
        update = Update(
            update_id=42,
            purchased_paid_media=PaidMediaPurchased(
                from_user={"id": 42, "is_bot": False, "first_name": "Test"},
                paid_media_payload="payload",
            ),
        )
        assert update.event_type == "purchased_paid_media"

    def test_roundtrip_uses_schema_name(self):
        update = Update(
            update_id=42,
            purchased_paid_media=PaidMediaPurchased(
                from_user={"id": 42, "is_bot": False, "first_name": "Test"},
                paid_media_payload="payload",
            ),
        )
        dumped = update.model_dump(exclude_none=True)
        assert "purchased_paid_media" in dumped
        assert "paid_media_purchased" not in dumped
