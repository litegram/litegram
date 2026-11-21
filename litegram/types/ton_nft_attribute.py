from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class TonNftAttribute(TelegramObject):
    """
    This object represents an attribute of an NFT in the TON blockchain.

    Source: https://core.telegram.org/bots/api#tonnftattribute
    """

    trait_type: str
    """Trait type of the attribute"""
    value: str
    """Value of the attribute"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(__pydantic__self__, *, trait_type: str, value: str, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(trait_type=trait_type, value=value, **__pydantic_kwargs)
