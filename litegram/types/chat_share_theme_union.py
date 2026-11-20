from __future__ import annotations

from typing import TypeAlias

from .chat_share_theme_emoji import ChatShareThemeEmoji
from .chat_share_theme_unique_gift import ChatShareThemeUniqueGift

type ChatShareThemeUnion = ChatShareThemeEmoji | ChatShareThemeUniqueGift
