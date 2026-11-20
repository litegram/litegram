from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import EmojiTypeType
from .emoji_type import EmojiType


class EmojiTypeEmoji(EmojiType):
    """
    A regular emoji.

    Source: https://core.telegram.org/bots/api#emojitypeemoji
    """

    type: Literal[EmojiTypeType.EMOJI] = EmojiTypeType.EMOJI
    """Type of the emoji, always 'emoji'"""
    emoji: str
    """The emoji"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            emoji: str,
            type: Literal[EmojiTypeType.EMOJI] = EmojiTypeType.EMOJI,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, emoji=emoji, **__pydantic_kwargs)
