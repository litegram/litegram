from __future__ import annotations

from enum import Enum


class EmojiTypeType(str, Enum):
    """
    This object represents the type of a emojitype object.

    Source: https://core.telegram.org/bots/api#emojitype
    """

    CUSTOM_EMOJI = "custom_emoji"
    EMOJI = "emoji"
