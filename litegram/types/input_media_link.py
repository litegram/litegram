from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class InputMediaLink(TelegramObject):
    """
    Represents an HTTP link to be sent.

    Source: https://core.telegram.org/bots/api#inputmedialink
    """

    type: str
    """Type of the media, must be *link*"""
    url: str
    """HTTP URL of the link"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(__pydantic__self__, *, type: str, url: str, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, url=url, **__pydantic_kwargs)
