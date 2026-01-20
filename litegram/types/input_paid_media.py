from __future__ import annotations

from .base import TelegramObject


class InputPaidMedia(TelegramObject):
    """
    This object describes the paid media to be sent. Currently, it can be one of

     - :class:`litegram.types.input_paid_media_photo.InputPaidMediaPhoto`
     - :class:`litegram.types.input_paid_media_video.InputPaidMediaVideo`

    Source: https://core.telegram.org/bots/api#inputpaidmedia
    """
