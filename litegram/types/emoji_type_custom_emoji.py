from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import EmojiTypeType
from .emoji_type import EmojiType


class EmojiTypeCustomEmoji(EmojiType):
    """
    A custom emoji.

    Source: https://core.telegram.org/bots/api#emojitypecustomemoji
    """

    type: Literal[EmojiTypeType.CUSTOM_EMOJI] = EmojiTypeType.CUSTOM_EMOJI
    """Type of the emoji, always 'custom_emoji'"""
    custom_emoji_id: str
    """Identifier of the custom emoji. Use :class:`litegram.methods.get_custom_emoji_stickers.GetCustomEmojiStickers` to get full information about the sticker."""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            custom_emoji_id: str,
            type: Literal[EmojiTypeType.CUSTOM_EMOJI] = EmojiTypeType.CUSTOM_EMOJI,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, custom_emoji_id=custom_emoji_id, **__pydantic_kwargs)
