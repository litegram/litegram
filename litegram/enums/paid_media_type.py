from __future__ import annotations

from enum import Enum


class PaidMediaType(str, Enum):
    """
    This object represents the type of a media in a paid message.

    Source: https://core.telegram.org/bots/api#paidmedia
    """

    LIVE_PHOTO = "live_photo"
    PHOTO = "photo"
    PREVIEW = "preview"
    VIDEO = "video"
