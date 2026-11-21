from litegram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from litegram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def test_inline_markup_options_survive_copy_and_can_be_overridden() -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[], force_reply=True)
    builder = InlineKeyboardBuilder.from_markup(markup).copy()
    assert builder.as_markup().force_reply is True
    assert builder.as_markup(force_reply=False).force_reply is False


def test_reply_markup_options_survive_copy_and_can_be_overridden() -> None:
    markup = ReplyKeyboardMarkup(keyboard=[], resize_keyboard=True, input_field_placeholder="Choose")
    builder = ReplyKeyboardBuilder.from_markup(markup).copy()
    assert builder.as_markup() == markup
    assert builder.as_markup(resize_keyboard=False).resize_keyboard is False
