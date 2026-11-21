from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichTextType
from .rich_text import RichText


class RichTextCustomEmoji(RichText):
    """
    A custom emoji.

    Source: https://core.telegram.org/bots/api#richtextcustomemoji
    """

    type: Literal[RichTextType.CUSTOM_EMOJI] = RichTextType.CUSTOM_EMOJI
    """Type of the rich text, always 'custom_emoji'"""
    custom_emoji_id: str
    """Unique identifier of the custom emoji. Use :class:`litegram.methods.get_custom_emoji_stickers.GetCustomEmojiStickers` to get full information about the sticker."""
    alternative_text: str
    """Alternative emoji for the custom emoji"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            custom_emoji_id: str,
            alternative_text: str,
            type: Literal[RichTextType.CUSTOM_EMOJI] = RichTextType.CUSTOM_EMOJI,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, custom_emoji_id=custom_emoji_id, alternative_text=alternative_text, **__pydantic_kwargs)
