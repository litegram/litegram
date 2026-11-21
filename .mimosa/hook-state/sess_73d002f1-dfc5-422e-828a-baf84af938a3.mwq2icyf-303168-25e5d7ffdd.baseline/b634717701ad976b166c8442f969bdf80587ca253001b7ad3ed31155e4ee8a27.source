from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject

if TYPE_CHECKING:
    from .live_photo import LivePhoto


class PaidMediaLivePhoto(TelegramObject):
    """
    The paid media is a `live photo <https://core.telegram.org/bots/api#livephoto>`_.

    Source: https://core.telegram.org/bots/api#paidmedialivephoto
    """

    type: str
    """Type of the paid media, always 'live_photo'"""
    live_photo: LivePhoto
    """The photo"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(__pydantic__self__, *, type: str, live_photo: LivePhoto, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, live_photo=live_photo, **__pydantic_kwargs)
