from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..types import File
from .base import TelegramMethod


class GetFile(TelegramMethod[File]):
    """
    Use this method to get basic information about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a :class:`litegram.types.file.File` object is returned. The file can then be downloaded via the link :code:`https://api.telegram.org/file/bot<token>/<file_path>`, where :code:`<file_path>` is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling :class:`litegram.methods.get_file.GetFile` again.

    Source: https://core.telegram.org/bots/api#getfile
    """

    __returning__ = File
    __api_method__ = "getFile"

    file_id: str
    """File identifier to get information about"""
    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via the litegram api tool

        def __init__(__pydantic__self__, *, file_id: str, **__pydantic_kwargs: Any) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via the litegram api tool
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(file_id=file_id, **__pydantic_kwargs)
