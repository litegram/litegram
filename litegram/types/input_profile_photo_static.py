from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from litegram.enums import InputProfilePhotoType

from .input_profile_photo import InputProfilePhoto

if TYPE_CHECKING:
    from .input_file_union import InputFileUnion


class InputProfilePhotoStatic(InputProfilePhoto):
    """
    A static profile photo in the .JPG format.

    Source: https://core.telegram.org/bots/api#inputprofilephotostatic
    """

    type: Literal[InputProfilePhotoType.STATIC] = InputProfilePhotoType.STATIC
    """Type of the profile photo, must be *static*"""
    photo: InputFileUnion
    """The static profile photo. Profile photos can't be reused and can only be uploaded as a new file, so you can pass 'attach://' if the photo was uploaded using multipart/form-data under . :ref:`More information on Sending Files » <sending-files>`"""
    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            photo: InputFileUnion,
            type: Literal[InputProfilePhotoType.STATIC] = InputProfilePhotoType.STATIC,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(type=type, photo=photo, **__pydantic_kwargs)
