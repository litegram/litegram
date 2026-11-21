from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichBlockType
from .rich_block import RichBlock

if TYPE_CHECKING:
    from .rich_block_union import RichBlockUnion
    from .rich_text_union import RichTextUnion


class RichBlockBlockQuotation(RichBlock):
    """
    A block quotation, corresponding to the HTML tag :code:`<blockquote>`.

    Source: https://core.telegram.org/bots/api#richblockblockquotation
    """

    type: Literal[RichBlockType.BLOCKQUOTE] = RichBlockType.BLOCKQUOTE
    """Type of the block, always 'blockquote'"""
    blocks: list[RichBlockUnion]
    """Content of the block"""
    credit: RichTextUnion | None = None
    """*Optional*. Credit of the block"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            blocks: list[RichBlockUnion],
            type: Literal[RichBlockType.BLOCKQUOTE] = RichBlockType.BLOCKQUOTE,
            credit: RichTextUnion | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, blocks=blocks, credit=credit, **__pydantic_kwargs)
