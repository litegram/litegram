from __future__ import annotations

from typing import TypeAlias

from .input_media_audio import InputMediaAudio
from .input_media_document import InputMediaDocument
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo

type MediaUnion = InputMediaAudio | InputMediaDocument | InputMediaPhoto | InputMediaVideo
