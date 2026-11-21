from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichTextType
from .rich_text import RichText

if TYPE_CHECKING:
    from .rich_text_union import RichTextUnion
    from .user import User


class RichTextTextMention(RichText):
    """
    A mention of a Telegram user by their identifier.

    Source: https://core.telegram.org/bots/api#richtexttextmention
    """

    type: Literal[RichTextType.TEXT_MENTION] = RichTextType.TEXT_MENTION
    """Type of the rich text, always 'text_mention'"""
    text: RichTextUnion
    """The text"""
    user: User
    """The mentioned user"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            text: RichTextUnion,
            user: User,
            type: Literal[RichTextType.TEXT_MENTION] = RichTextType.TEXT_MENTION,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, text=text, user=user, **__pydantic_kwargs)
