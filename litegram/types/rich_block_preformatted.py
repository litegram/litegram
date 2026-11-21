from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import RichBlockType
from .rich_block import RichBlock

if TYPE_CHECKING:
    from .rich_text_union import RichTextUnion


class RichBlockPreformatted(RichBlock):
    """
    A preformatted text block, corresponding to the nested HTML tags :code:`<pre>` and :code:`<code>`.

    Source: https://core.telegram.org/bots/api#richblockpreformatted
    """

    type: Literal[RichBlockType.PRE] = RichBlockType.PRE
    """Type of the block, always 'pre'"""
    text: RichTextUnion
    """Text of the block"""
    language: str | None = None
    """*Optional*. The programming language of the text"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            text: RichTextUnion,
            type: Literal[RichBlockType.PRE] = RichBlockType.PRE,
            language: str | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, text=text, language=language, **__pydantic_kwargs)
