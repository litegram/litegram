"""Consistency test: UpdateType enum mirrors the Update schema fields."""

from __future__ import annotations

from litegram.enums import UpdateType
from litegram.types import Update


def test_update_type_mirrors_update_fields():
    field_names = {name for name in Update.model_fields if name != "update_id"}
    enum_values = {member.value for member in UpdateType}
    assert field_names == enum_values
