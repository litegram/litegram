from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import ChatShareThemeType
from .chat_share_theme import ChatShareTheme

if TYPE_CHECKING:
    from .unique_gift import UniqueGift


class ChatShareThemeUniqueGift(ChatShareTheme):
    """
    The theme based on a unique gift owned by the user or the chat.

    Source: https://core.telegram.org/bots/api#chatsharethemeuniquegift
    """

    type: Literal[ChatShareThemeType.UNIQUE_GIFT] = ChatShareThemeType.UNIQUE_GIFT
    """Type of the theme, always 'unique_gift'"""
    gift: UniqueGift
    """The gift"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            gift: UniqueGift,
            type: Literal[ChatShareThemeType.UNIQUE_GIFT] = ChatShareThemeType.UNIQUE_GIFT,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, gift=gift, **__pydantic_kwargs)
