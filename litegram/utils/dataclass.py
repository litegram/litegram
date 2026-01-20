"""
This module contains utility functions for working with dataclasses in Python.

DO NOT USE THIS MODULE DIRECTLY. IT IS INTENDED FOR INTERNAL USE ONLY.
"""

from __future__ import annotations

from typing import Any


def dataclass_kwargs(
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    match_args: bool = True,
    kw_only: bool = False,
    slots: bool = False,
    weakref_slot: bool = False,
) -> dict[str, Any]:
    """
    Generates a dictionary of keyword arguments that can be passed to a Python
    dataclass.

    :return: A dictionary containing the specified dataclass configuration.
    """
    return {
        "init": init,
        "repr": repr,
        "eq": eq,
        "order": order,
        "unsafe_hash": unsafe_hash,
        "frozen": frozen,
        "match_args": match_args,
        "kw_only": kw_only,
        "slots": slots,
        "weakref_slot": weakref_slot,
    }
