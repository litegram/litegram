from __future__ import annotations

from .base import MutableTelegramObject


class InlineQueryResult(MutableTelegramObject):
    """
    This object represents one result of an inline query. Telegram clients currently support results of the following 20 types:

     - :class:`litegram.types.inline_query_result_cached_audio.InlineQueryResultCachedAudio`
     - :class:`litegram.types.inline_query_result_cached_document.InlineQueryResultCachedDocument`
     - :class:`litegram.types.inline_query_result_cached_gif.InlineQueryResultCachedGif`
     - :class:`litegram.types.inline_query_result_cached_mpeg4_gif.InlineQueryResultCachedMpeg4Gif`
     - :class:`litegram.types.inline_query_result_cached_photo.InlineQueryResultCachedPhoto`
     - :class:`litegram.types.inline_query_result_cached_sticker.InlineQueryResultCachedSticker`
     - :class:`litegram.types.inline_query_result_cached_video.InlineQueryResultCachedVideo`
     - :class:`litegram.types.inline_query_result_cached_voice.InlineQueryResultCachedVoice`
     - :class:`litegram.types.inline_query_result_article.InlineQueryResultArticle`
     - :class:`litegram.types.inline_query_result_audio.InlineQueryResultAudio`
     - :class:`litegram.types.inline_query_result_contact.InlineQueryResultContact`
     - :class:`litegram.types.inline_query_result_game.InlineQueryResultGame`
     - :class:`litegram.types.inline_query_result_document.InlineQueryResultDocument`
     - :class:`litegram.types.inline_query_result_gif.InlineQueryResultGif`
     - :class:`litegram.types.inline_query_result_location.InlineQueryResultLocation`
     - :class:`litegram.types.inline_query_result_mpeg4_gif.InlineQueryResultMpeg4Gif`
     - :class:`litegram.types.inline_query_result_photo.InlineQueryResultPhoto`
     - :class:`litegram.types.inline_query_result_venue.InlineQueryResultVenue`
     - :class:`litegram.types.inline_query_result_video.InlineQueryResultVideo`
     - :class:`litegram.types.inline_query_result_voice.InlineQueryResultVoice`

    **Note:** All URLs passed in inline query results will be available to end users and therefore must be assumed to be **public**.

    Source: https://core.telegram.org/bots/api#inlinequeryresult
    """
