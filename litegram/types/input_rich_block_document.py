from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import InputRichBlockType
from .input_rich_block import InputRichBlock

if TYPE_CHECKING:
    from .input_media_document import InputMediaDocument
    from .rich_block_caption import RichBlockCaption


class InputRichBlockDocument(InputRichBlock):
    """
    A block with a general file, corresponding to the custom HTML tag :code:`<tg-document>`.

    Source: https://core.telegram.org/bots/api#inputrichblockdocument
    """

    type: Literal[InputRichBlockType.DOCUMENT] = InputRichBlockType.DOCUMENT
    """Type of the block, always 'document'"""
    document: InputMediaDocument
    """The document. Caption is ignored."""
    caption: RichBlockCaption | None = None
    """*Optional*. Caption of the block"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            document: InputMediaDocument,
            type: Literal[InputRichBlockType.DOCUMENT] = InputRichBlockType.DOCUMENT,
            caption: RichBlockCaption | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, document=document, caption=caption, **__pydantic_kwargs)
