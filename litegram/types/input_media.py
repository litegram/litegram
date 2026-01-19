from __future__ import annotations

from .base import MutableTelegramObject


class InputMedia(MutableTelegramObject):
    """
    This object represents the content of a media message to be sent. It should be one of

     - :class:`litegram.types.input_media_animation.InputMediaAnimation`
     - :class:`litegram.types.input_media_document.InputMediaDocument`
     - :class:`litegram.types.input_media_audio.InputMediaAudio`
     - :class:`litegram.types.input_media_photo.InputMediaPhoto`
     - :class:`litegram.types.input_media_video.InputMediaVideo`

    Source: https://core.telegram.org/bots/api#inputmedia
    """
