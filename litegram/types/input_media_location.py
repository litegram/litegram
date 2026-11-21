from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class InputMediaLocation(TelegramObject):
    """
    Represents a location to be sent.

    Source: https://core.telegram.org/bots/api#inputmedialocation
    """

    type: str
    """Type of the media, must be *location*"""
    latitude: float
    """Latitude of the location"""
    longitude: float
    """Longitude of the location"""
    horizontal_accuracy: float | None = None
    """*Optional*. The radius of uncertainty for the location, measured in meters; 0-1500"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(
            __pydantic__self__,
            *,
            type: str,
            latitude: float,
            longitude: float,
            horizontal_accuracy: float | None = None,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                type=type,
                latitude=latitude,
                longitude=longitude,
                horizontal_accuracy=horizontal_accuracy,
                **__pydantic_kwargs,
            )
