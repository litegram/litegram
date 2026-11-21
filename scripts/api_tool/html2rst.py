"""HTML -> reStructuredText conversion for Telegram Bot API descriptions.

The Bot API page is the single source of truth for both generated code
docstrings and the Sphinx docs, so descriptions are converted to RST once
at parse time and stored in the schema.

The rules mirror the original generator's converter so that the diff against
previously generated content stays minimal:

- ``<a href="#anchor">``          -> ``:class:`litegram.types.x.Y`` for known
                                     object anchors, otherwise an external link
                                     to ``https://core.telegram.org/bots/api#anchor``
- ``<a href="https://...">``      -> `` `text <url>`_ ``
- ``<strong>/<b>``                -> ``**text**``
- ``<em>/<i>``                    -> ``*text*``
- ``<code>``                      -> ``:code:`text``
- ``<br>``                        -> paragraph break
- ``<p>``                         -> paragraph separation
- ``<ul>/<li>``                   -> ``- item`` bullet lines
- ``<blockquote>``                -> indented block
- emoji ``<img>``                 -> the ``alt`` character
- HTML entities                   -> unicode equivalents, curly quotes -> straight
"""

from __future__ import annotations

import re
from html import unescape
from html.parser import HTMLParser

API_URL = "https://core.telegram.org/bots/api"

# Block-level tags that separate RST blocks.
_BLOCK_TAGS = frozenset({"p", "ul", "ol", "blockquote", "table"})
# Tags that do not produce any output by themselves.
_VOID_TAGS = frozenset({"img", "br", "hr", "input"})

QUOTE_MAP = {
    "\u201c": "'",  # left double quotation mark
    "\u201d": "'",  # right double quotation mark
    "\u2018": "'",  # left single quotation mark
    "\u2019": "'",  # right single quotation mark
}

_CURLY_QUOTE_RE = re.compile("[\u201c\u201d\u2018\u2019]")


def normalize_text(text: str) -> str:
    """Normalize unicode quotes and collapse consecutive whitespace."""
    return _CURLY_QUOTE_RE.sub(lambda m: QUOTE_MAP[m.group(0)], text)


class _Node:
    """A lightweight DOM-ish node produced by the tree builder."""

    __slots__ = ("tag", "attrs", "children")

    def __init__(self, tag: str, attrs: list[tuple[str, str | None]] | None = None) -> None:
        self.tag = tag
        self.attrs = {k or "": (v or "") for k, v in (attrs or [])}
        self.children: list[_Node | str] = []

    def get_text(self) -> str:
        parts = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                parts.append(child.get_text())
        return "".join(parts)


class _TreeBuilder(HTMLParser):
    """Builds a simple document tree, tolerating void tags and mis-nesting."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Node("#root")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Nested anchors are invalid HTML. Browsers implicitly close the outer
        # link, and the Bot API page occasionally relies on that behavior.
        if tag == "a":
            for i in range(len(self.stack) - 1, 0, -1):
                if self.stack[i].tag == "a":
                    del self.stack[i:]
                    break
        node = _Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in _VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = _Node(tag, attrs)
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        # Unwind to the matching open tag (self-heal on mis-nesting).
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].children.append(data)


class KnownObject:
    """A parsed API object that inline links may reference."""

    __slots__ = ("name", "namespace")

    def __init__(self, name: str, namespace: str) -> None:
        self.name = name
        self.namespace = namespace

    @property
    def class_name(self) -> str:
        # Method objects are named in lowerCamelCase on the docs page
        # (e.g. "getMe") but the generated classes are CamelCase (GetMe).
        if self.namespace == "methods" and self.name[:1].islower():
            return self.name[:1].upper() + self.name[1:]
        return self.name

    def class_ref(self) -> str:
        module = _snake_case(self.class_name)
        return f":class:`litegram.{self.namespace}.{module}.{self.class_name}`"


class RstConverter:
    """Converts a Bot API HTML fragment into RST.

    ``known_objects`` maps object anchors (lowercase, e.g. ``"message"``)
    to :class:`KnownObject`; links pointing at them are rendered as
    ``:class:`` references instead of plain URLs.
    """

    def __init__(self, known_objects: dict[str, KnownObject]) -> None:
        self.known_objects = known_objects

    def convert(self, html: str, *, strip_td: bool = False, strip_p: bool = False) -> str:
        """Convert an HTML fragment to RST text."""
        if strip_td:
            html = re.sub(r"^\s*<td>|</td>\s*$", "", html.strip())
        if strip_p:
            html = re.sub(r"^\s*<p>|</p>\s*$", "", html.strip())
        builder = _TreeBuilder()
        builder.feed(html)
        builder.close()
        parts = self._render_children(builder.root.children)
        return self._cleanup("".join(parts))

    # --- rendering ---------------------------------------------------------

    def _render_children(self, children: list[_Node | str]) -> list[str]:
        out: list[str] = []
        for node in children:
            if isinstance(node, str):
                out.append(self._escape_text(node))
            else:
                out.append(self._render_node(node))
        return out

    def _render_node(self, node: _Node) -> str:
        tag = node.tag
        if tag == "a":
            return self._render_link(node)
        if tag in {"strong", "b"}:
            inner = "".join(self._render_children(node.children))
            return f"**{inner.strip()}**"
        if tag in {"em", "i"}:
            inner = "".join(self._render_children(node.children)).strip()
            # "True"/"False" markers describe literal JSON values, not emphasis.
            if inner in {"True", "False"}:
                return f":code:`{inner}`"
            return f"*{inner}*"
        if tag == "code":
            inner = "".join(self._render_children(node.children))
            return f":code:`{inner.strip()}`"
        if tag == "img":
            return node.attrs.get("alt", "")
        if tag == "br":
            return "\n\n"
        if tag in _BLOCK_TAGS:
            return self._render_block(node)
        # Unknown/inline containers (span, s, del, ...): transparent.
        return "".join(self._render_children(node.children))

    def _render_link(self, node: _Node) -> str:
        href = (node.attrs.get("href") or "").strip()
        text = "".join(self._render_children(node.children)).strip()
        if not text:
            return ""
        if href.startswith("#"):
            anchor = href[1:].lower()
            if anchor == "sending-files" and text.startswith("More information on Sending Files"):
                # Cross-reference the litegram upload guide (docs/api/upload_file.rst).
                return f":ref:`{text} <sending-files>`"
            known = self.known_objects.get(anchor)
            # Legacy converter behaviour: render a :class: reference only when
            # the link text is the object name itself (e.g. "Message"), keep
            # prose links ("webhooks", "emoji reactions") as plain URLs.
            if known is not None and text.lower() == known.name.lower():
                return known.class_ref()
            return f"`{text} <{API_URL}#{anchor}>`_"
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = API_URL.removesuffix("/bots/api") + href
        return f"`{text} <{href}>`_"

    def _render_block(self, node: _Node) -> str:
        if node.tag == "blockquote":
            inner = "".join(self._render_children(node.children))
            lines = inner.strip().splitlines()
            indented = "\n".join(" " + line for line in lines)
            return "\n\n" + indented + "\n"
        if node.tag in {"ul", "ol"}:
            items = []
            for child in node.children:
                if isinstance(child, _Node) and child.tag == "li":
                    rendered = "".join(self._render_children(child.children)).strip()
                    items.append(f" - {rendered}")
            return "\n\n" + "\n".join(items) + "\n"
        # <p> and similar: paragraphs separated by blank lines.
        inner = "".join(self._render_children(node.children)).strip()
        return "\n\n" + inner

    # --- post processing ----------------------------------------------------

    def _escape_text(self, text: str) -> str:
        return normalize_text(text)

    def _cleanup(self, text: str) -> str:
        # Collapse 3+ blank lines to a single paragraph break.
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Trim spaces before newlines and drop leading/trailing blank lines.
        lines = [line.rstrip() for line in text.split("\n")]
        return "\n".join(lines).strip("\n")


class TextConverter(RstConverter):
    """Plain-text variant: markup is dropped, structure kept minimal.

    Mirrors the legacy ``description`` field conventions:

    - links/strong/em/code render as their inner text
    - ``<br>`` -> single newline, ``<p>`` -> blank-line separated
    - lists render as ``- item`` lines
    """

    def _render_link(self, node: _Node) -> str:
        return "".join(self._render_children(node.children)).strip()

    def _render_node(self, node: _Node) -> str:
        tag = node.tag
        if tag == "br":
            return "\n"
        if tag in {"strong", "b", "em", "i", "code", "span"}:
            return "".join(self._render_children(node.children))
        if tag == "img":
            return node.attrs.get("alt", "")
        if tag == "blockquote":
            inner = "".join(self._render_children(node.children)).strip()
            return "\n" + inner
        if tag in {"ul", "ol"}:
            items = []
            for child in node.children:
                if isinstance(child, _Node) and child.tag == "li":
                    rendered = "".join(self._render_children(child.children)).strip()
                    items.append(f" - {rendered}")
            return "\n" + "\n".join(items)
        if tag == "p":
            inner = "".join(self._render_children(node.children)).strip()
            return "\n\n" + inner
        return "".join(self._render_children(node.children))

    def _cleanup(self, text: str) -> str:
        text = re.sub(r"\n{3,}", "\n\n", text)
        lines = [line.rstrip() for line in text.split("\n")]
        return "\n".join(lines).strip("\n")


def _snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def default_known_objects(types: list[str], methods: list[str]) -> dict[str, KnownObject]:
    """Build the anchor -> KnownObject mapping from parsed object names."""
    known: dict[str, KnownObject] = {}
    for name in types:
        known[name.lower()] = KnownObject(name, "types")
    for name in methods:
        known[name.lower()] = KnownObject(name, "methods")
    return known
