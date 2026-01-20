from __future__ import annotations

from typing import TypeAlias

from .input_profile_photo_animated import InputProfilePhotoAnimated
from .input_profile_photo_static import InputProfilePhotoStatic

type InputProfilePhotoUnion = InputProfilePhotoStatic | InputProfilePhotoAnimated
