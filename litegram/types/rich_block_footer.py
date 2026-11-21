from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichBlockType
from .rich_block import RichBlock

if TYPE_CHECKING:
    from .rich_text_union import RichTextUnion


class RichBlockFooter(RichBlock):
    """
    A footer, corresponding to the HTML tag :code:`<footer>`.

    Source: https://core.telegram.org/bots/api#richblockfooter
    """

    type: Literal[RichBlockType.FOOTER] = RichBlockType.FOOTER
    """Type of the block, always 'footer'"""
    text: RichTextUnion
    """Text of the block"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            text: RichTextUnion,
            type: Literal[RichBlockType.FOOTER] = RichBlockType.FOOTER,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, text=text, **__pydantic_kwargs)
