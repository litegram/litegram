from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichTextType
from .rich_text import RichText

if TYPE_CHECKING:
    from .rich_text_union import RichTextUnion


class RichTextSuperscript(RichText):
    """
    A superscript text.

    Source: https://core.telegram.org/bots/api#richtextsuperscript
    """

    type: Literal[RichTextType.SUPERSCRIPT] = RichTextType.SUPERSCRIPT
    """Type of the rich text, always 'superscript'"""
    text: RichTextUnion
    """The text"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            text: RichTextUnion,
            type: Literal[RichTextType.SUPERSCRIPT] = RichTextType.SUPERSCRIPT,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, text=text, **__pydantic_kwargs)
