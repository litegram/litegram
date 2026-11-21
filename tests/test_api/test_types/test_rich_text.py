"""Behavioral tests for the RichText/RichBlock families introduced in Bot API 10.0."""

from __future__ import annotations

from typing import Any, cast

from pydantic import TypeAdapter

from litegram.enums import RichTextType
from litegram.types import (
    RichTextBold,
    RichTextItalic,
    RichTextUnion,
)


class TestRichTextUnion:
    """The recursive union accepts plain strings, lists and all variants."""

    def test_plain_string(self):
        adapter = TypeAdapter(RichTextUnion)
        assert adapter.validate_python("hello") == "hello"

    def test_list_of_variants(self):
        adapter = TypeAdapter(RichTextUnion)
        result = cast(
            "list[Any]",
            adapter.validate_python(
                [
                    "plain ",
                    {"type": "bold", "text": "bold text"},
                ]
            ),
        )
        assert isinstance(result[0], str)
        assert isinstance(result[1], RichTextBold)
        assert result[1].type == RichTextType.BOLD

    def test_recursive_nesting(self):
        """Nested rich text structures round-trip through the union."""
        adapter = TypeAdapter(RichTextUnion)
        result = adapter.validate_python(
            {
                "type": "italic",
                "text": [
                    {"type": "bold", "text": "nested"},
                ],
            }
        )
        assert isinstance(result, RichTextItalic)
        text = cast("list[Any]", result.text)
        assert isinstance(text[0], RichTextBold)

    def test_discriminator_field_is_literal(self):
        bold = RichTextBold(text="x")
        assert bold.type == RichTextType.BOLD
        assert bold.model_dump()["type"] == "bold"
