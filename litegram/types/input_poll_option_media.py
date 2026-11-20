from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import TelegramObject


class InputPollOptionMedia(TelegramObject):
    """
    This object represents the content of a poll option to be sent. It should be one of

     - :class:`litegram.types.input_media_animation.InputMediaAnimation`
     - :class:`litegram.types.input_media_link.InputMediaLink`
     - :class:`litegram.types.input_media_live_photo.InputMediaLivePhoto`
     - :class:`litegram.types.input_media_location.InputMediaLocation`
     - :class:`litegram.types.input_media_photo.InputMediaPhoto`
     - :class:`litegram.types.input_media_sticker.InputMediaSticker`
     - :class:`litegram.types.input_media_venue.InputMediaVenue`
     - :class:`litegram.types.input_media_video.InputMediaVideo`

    Source: https://core.telegram.org/bots/api#inputpolloptionmedia
    """
