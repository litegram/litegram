from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class ChatShareTheme(TelegramObject):
    """
    This object describes the theme of the screen for sharing a link to a user or a chat. Currently, it can be one of

     - :class:`litegram.types.chat_share_theme_emoji.ChatShareThemeEmoji`
     - :class:`litegram.types.chat_share_theme_unique_gift.ChatShareThemeUniqueGift`

    Source: https://core.telegram.org/bots/api#chatsharetheme
    """
