from __future__ import annotations

from enum import Enum


class ChatShareThemeType(str, Enum):
    """
    This object represents the type of a chatsharetheme object.

    Source: https://core.telegram.org/bots/api#chatsharetheme
    """

    EMOJI = "emoji"
    UNIQUE_GIFT = "unique_gift"
