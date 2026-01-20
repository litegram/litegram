from __future__ import annotations

from litegram.utils.dataclass import dataclass_kwargs

ALL_VERSIONS = {
    "init": True,
    "repr": True,
    "eq": True,
    "order": True,
    "unsafe_hash": True,
    "frozen": True,
    "match_args": True,
    "kw_only": True,
    "slots": True,
    "weakref_slot": True,
}


class TestDataclassKwargs:
    def test_dataclass_kwargs(self):
        assert (
            dataclass_kwargs(
                init=True,
                repr=True,
                eq=True,
                order=True,
                unsafe_hash=True,
                frozen=True,
                match_args=True,
                kw_only=True,
                slots=True,
                weakref_slot=True,
            )
            == ALL_VERSIONS
        )
