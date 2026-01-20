from __future__ import annotations

from typing import Any, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class AttrDict(dict[KT, VT]):
    """
    A wrapper over dict which where element can be accessed as regular attributes
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__dict__ = self  # type: ignore
