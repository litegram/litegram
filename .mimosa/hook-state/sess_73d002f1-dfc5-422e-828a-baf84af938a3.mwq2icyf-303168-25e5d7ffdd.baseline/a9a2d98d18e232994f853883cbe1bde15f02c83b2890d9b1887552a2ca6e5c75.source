from __future__ import annotations

from litegram.utils.markdown import hlink, hide_link, link
from litegram.utils.text_decorations import HtmlDecoration, MarkdownDecoration


class TestUrlEscaping:
    """URLs go into HTML attributes and Markdown groups: they must be escaped."""

    def test_hlink_escapes_attribute_injection(self):
        url = 'https://example.test" onmouseover="alert(1)'
        result = hlink("test", url)
        assert '" onmouseover' not in result
        assert "&quot;" in result

    def test_hide_link_escapes_attribute_injection(self):
        url = 'https://example.test" style="x'
        result = hide_link(url)
        # The raw quote must be escaped inside the href attribute.
        assert 'href="https://example.test&quot;' in result
        assert 'style=&quot;x' in result

    def test_markdown_link_escapes_closing_paren(self):
        url = "https://example.test/a)b"
        result = link("test", url)
        assert result == r"[test](https://example.test/a\)b)"

    def test_markdown_link_escapes_backslash(self):
        result = link("test", "https://example.test/a\\b")
        assert result == r"[test](https://example.test/a\\b)"

    def test_html_pre_language_rejects_unsafe_tag(self):
        decoration = HtmlDecoration()
        assert decoration.pre_language("x", "py<script>") == "<pre>x</pre>"
        assert decoration.pre_language("x", "py\ninjected") == "<pre>x</pre>"
        assert decoration.pre_language("x", "py3.13") == '<pre><code class="language-py3.13">x</code></pre>'

    def test_markdown_pre_language_rejects_unsafe_tag(self):
        decoration = MarkdownDecoration()
        assert decoration.pre_language("x", "bad`\n fence") == "```\nx\n```"
        assert decoration.pre_language("x", "py3") == "```py3\nx\n```"
