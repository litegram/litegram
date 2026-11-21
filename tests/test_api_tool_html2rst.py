from __future__ import annotations

from scripts.api_tool.html2rst import RstConverter


def test_nested_anchor_is_closed_like_html5():
    html = (
        'See <a href="/stickers">'
        '<a href="https://core.telegram.org/stickers">https://core.telegram.org/stickers</a>'
        "</a> for technical requirements."
    )

    result = RstConverter({}).convert(html)

    assert result == (
        "See `https://core.telegram.org/stickers <https://core.telegram.org/stickers>`_ for technical requirements."
    )


def test_empty_anchor_does_not_render_rst_markup():
    assert RstConverter({}).convert('<a href="https://example.com"></a>') == ""
