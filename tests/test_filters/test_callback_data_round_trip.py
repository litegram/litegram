"""Documented round-trip semantics for callback data packing."""

from __future__ import annotations

from litegram.filters.callback_data import CallbackData, MAX_CALLBACK_LENGTH


class Shipping(CallbackData, prefix="ship"):
    option_id: str
    note: str | None = None
    quantity: int | None = 1


class TestCallbackDataRoundTrip:
    def test_basic_round_trip(self):
        callback = Shipping(option_id="express", note="ring twice", quantity=2)
        unpacked = Shipping.unpack(callback.pack())
        assert unpacked == callback

    def test_none_field_without_default_round_trips_as_none(self):
        callback = Shipping(option_id="pick", note=None)
        unpacked = Shipping.unpack(callback.pack())
        assert unpacked.note is None
        # A field with a default gets the default: positional format cannot
        # carry an explicit None.
        assert unpacked.quantity == 1

    def test_empty_field_unpacks_to_field_default(self):
        # Positional string format cannot distinguish an explicit None from
        # an empty value: the field default wins on unpack.
        callback = Shipping(option_id="pick", note=None, quantity=None)
        assert callback.pack() == "ship:pick::"
        unpacked = Shipping.unpack(callback.pack())
        assert unpacked.quantity == 1
        assert unpacked.note is None

    def test_prefix_is_required(self):
        import pytest

        with pytest.raises(ValueError, match="prefix required"):
            type("Broken", (CallbackData,), {})

    def test_too_long_callback_data(self):
        import pytest

        callback = Shipping(option_id="x" * MAX_CALLBACK_LENGTH)
        with pytest.raises(ValueError, match="too long"):
            callback.pack()
