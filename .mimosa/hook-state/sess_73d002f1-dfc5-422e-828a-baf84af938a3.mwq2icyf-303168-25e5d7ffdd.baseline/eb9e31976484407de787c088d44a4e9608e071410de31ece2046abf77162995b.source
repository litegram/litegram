from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject

if TYPE_CHECKING:
    from .input_rich_block_union import InputRichBlockUnion
    from .input_rich_message_media_union import InputRichMessageMediaUnion


class InputRichMessage(TelegramObject):
    """
    Describes a rich message to be sent. Exactly **one** of the fields *html*, *markdown*, or *blocks* must be used.

    Source: https://core.telegram.org/bots/api#inputrichmessage
    """

    blocks: list[InputRichBlockUnion] | None = None
    """*Optional*. Content of the rich message to send described as a list of blocks"""
    html: str | None = None
    """*Optional*. Content of the rich message to send described using HTML formatting. See `rich message formatting options <https://core.telegram.org/bots/api#rich-message-formatting-options>`_ for more details. Use *media* field to specify the media used in the message."""
    markdown: str | None = None
    """*Optional*. Content of the rich message to send described using Markdown formatting. See `rich message formatting options <https://core.telegram.org/bots/api#rich-message-formatting-options>`_ for more details. Use *media* field to specify the media used in the message."""
    media: list[InputRichMessageMediaUnion] | None = None
    """*Optional*. List of media that are specified in the *markdown* or *html* fields using :code:`tg://photo?id=`, :code:`tg://video?id=`, :code:`tg://document?id=`, and :code:`tg://audio?id=` links"""
    is_rtl: bool | None = None
    """*Optional*. Pass :code:`True` if the rich message must be shown right-to-left"""
    skip_entity_detection: bool | None = None
    """*Optional*. Pass :code:`True` to skip automatic detection of entities (e.g., URLs, email addresses, username mentions, hashtags, cashtags, bot commands, or phone numbers) in the text"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            blocks: list[InputRichBlockUnion] | None = None,
            html: str | None = None,
            markdown: str | None = None,
            media: list[InputRichMessageMediaUnion] | None = None,
            is_rtl: bool | None = None,
            skip_entity_detection: bool | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                blocks=blocks,
                html=html,
                markdown=markdown,
                media=media,
                is_rtl=is_rtl,
                skip_entity_detection=skip_entity_detection,
                **__pydantic_kwargs,
            )
