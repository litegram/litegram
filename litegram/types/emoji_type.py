from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class EmojiType(TelegramObject):
    """
    This object describes an emoji. Currently, it can be one of

     - :class:`litegram.types.emoji_type_emoji.EmojiTypeEmoji`
     - :class:`litegram.types.emoji_type_custom_emoji.EmojiTypeCustomEmoji`

    Source: https://core.telegram.org/bots/api#emojitype
    """
