from __future__ import annotations

from .base import TelegramObject


class PaidMedia(TelegramObject):
    """
    This object describes paid media. Currently, it can be one of

     - :class:`litegram.types.paid_media_preview.PaidMediaPreview`
     - :class:`litegram.types.paid_media_photo.PaidMediaPhoto`
     - :class:`litegram.types.paid_media_video.PaidMediaVideo`

    Source: https://core.telegram.org/bots/api#paidmedia
    """
