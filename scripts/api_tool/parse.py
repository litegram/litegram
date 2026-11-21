"""Parse the Telegram Bot API documentation page into a structured schema.

Produces:
    - ``.api/schema.json``                    — the full schema (versioned cache)
    - ``.api/{types,methods}/<name>/entity.json`` — per-object caches used by
      the docs generator

The schema format is intentionally close to the legacy ``butcher`` cache so
that the previous schema (``.butcher/schema/schema.json``) can be diffed
against the new one.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .html2rst import RstConverter, TextConverter, _Node, _TreeBuilder, default_known_objects

METHOD_CELL_COUNT = 4
TYPE_CELL_COUNT = 3

PAGE_URL = "https://core.telegram.org/bots/api"

# Sections that contain object definitions (any h3 section with h4+table
# children is also picked up, this is just the canonical order).
SECTION_ORDER = (
    "getting-updates",
    "available-types",
    "available-methods",
    "updating-messages",
    "stickers",
    "inline-mode",
    "payments",
    "telegram-passport",
    "games",
)

_H3_RE = re.compile(
    r'<h3><a class="anchor" name="(?P<anchor>[^"]+)" href="#[^"]+">'
    r'<i class="anchor-icon"></i></a>(?P<title>[^<]+)</h3>'
)
_H4_RE = re.compile(
    r'<h4><a class="anchor" name="(?P<anchor>[^"]+)" href="#[^"]+">'
    r'<i class="anchor-icon"></i></a>(?P<name>[^<]+)</h4>'
)
_VERSION_RE = re.compile(r"<strong>Bot API (?P<version>\d+\.\d+)</strong>")
_DATE_H4_RE = re.compile(
    r"<h4><a class=\"anchor\" name=\"[^\"]+\" href=\"#([a-z]+-[\d-]+)\">"
    r"<i class=\"anchor-icon\"></i></a>(?P<human>[A-Z][a-z]+ \d{1,2}, \d{4})</h4>"
)


def extract_api_version(html: str) -> tuple[str, str]:
    """Extract ``(version, release_date)`` from the changelog head of the page."""
    version_match = _VERSION_RE.search(html)
    if not version_match:
        raise ValueError("Cannot find 'Bot API X.Y' marker on the page")
    version = version_match.group("version")

    # The newest changelog entry date is the h4 heading right before it.
    head = html[: version_match.start()]
    date_match = None
    for date_match in _DATE_H4_RE.finditer(head):  # noqa: B007 — last match used after loop
        pass
    if date_match is None:
        raise ValueError("Cannot find release date heading on the page")
    from datetime import UTC, datetime

    release_date = datetime.strptime(date_match.group("human"), "%B %d, %Y").replace(tzinfo=UTC).date().isoformat()
    return version, release_date


def _strip_td(html: str) -> str:
    return re.sub(r"^\s*<td>|</td>\s*$", "", html.strip())


def _html_to_text(html: str) -> str:
    """Extract plain text from a small HTML fragment."""
    builder = _TreeBuilder()
    builder.feed(html)
    builder.close()
    return normalize_quotes(builder.root.get_text())


def normalize_quotes(text: str) -> str:
    from .html2rst import normalize_text

    return normalize_text(text)


def _strip_p(html: str) -> str:
    return re.sub(r"^\s*<p>|</p>\s*$", "", html.strip())


def parse_table(table_html: str) -> tuple[list[str], list[list[str]]]:
    """Parse a docs table into header cells and rows of raw cell HTML."""
    builder = _TreeBuilder()
    builder.feed(table_html)
    builder.close()
    table = builder.root.children[0]
    headers: list[str] = []
    rows: list[list[str]] = []
    thead = next(
        (c for c in table.children if isinstance(c, _Node) and c.tag == "thead"),
        None,
    )
    if thead is not None:
        tr = next(
            (c for c in thead.children if isinstance(c, _Node) and c.tag == "tr"),
            None,
        )
        if tr is not None:
            headers = [c.get_text().strip() for c in tr.children if isinstance(c, _Node) and c.tag in {"th", "td"}]
    tbody = next(
        (c for c in table.children if isinstance(c, _Node) and c.tag == "tbody"),
        table,
    )
    for tr in tbody.children:
        if not isinstance(tr, _Node) or tr.tag != "tr":
            continue
        cells = ["".join(_cell_html(c)).strip() for c in tr.children if isinstance(c, _Node) and c.tag == "td"]
        if cells:
            rows.append(cells)
    return headers, rows


def _cell_html(node: _Node | str) -> list[str]:
    """Serialize a cell node back to compact HTML."""
    if isinstance(node, str):
        return [node]
    if node.tag == "br":
        return [f"<{node.tag}>"]
    attrs = "".join(f' {k}="{v}"' for k, v in node.attrs.items() if k != "#root")
    inner = "".join("".join(_cell_html(c)) for c in node.children)
    if not inner and node.tag == "img":
        return [f"<{node.tag}{attrs}/>"]
    return [f"<{node.tag}{attrs}>{inner}</{node.tag}>"]


def parse_page(html: str) -> dict[str, Any]:  # noqa: PLR0914 — parser keeps many local accumulators
    """Parse the whole Bot API page into the schema structure."""
    version, release_date = extract_api_version(html)

    # Collect all object names first so the RST converter can resolve links.
    h3_matches = list(_H3_RE.finditer(html))
    sections: list[tuple[str, str, int, int]] = [
        (
            m.group("anchor"),
            m.group("title").strip(),
            m.end(),
            h3_matches[i + 1].start() if i + 1 < len(h3_matches) else len(html),
        )
        for i, m in enumerate(h3_matches)
    ]

    names: list[str] = [
        hm.group("name") for _, _, sec_start, sec_end in sections for hm in _H4_RE.finditer(html, sec_start, sec_end)
    ]
    known = default_known_objects(
        [n for n in names if n[:1].isupper()],
        [n for n in names if not n[:1].isupper()],
    )
    converter = RstConverter(known)
    text_converter = TextConverter(known)

    items: list[dict[str, Any]] = []
    for anchor, title, sec_start, sec_end in sections:  # noqa: PLR1702 — nested parsing of sections/objects
        children: list[dict[str, Any]] = []
        h4_matches = list(_H4_RE.finditer(html, sec_start, sec_end))
        for i, hm in enumerate(h4_matches):
            obj_name = hm.group("name")
            if re.search(r"\s", obj_name):
                # Prose headings (changelog dates, FAQ subsections) are not
                # API objects — real object names never contain whitespace.
                continue
            obj_anchor = hm.group("anchor")
            block_start = hm.end()
            block_end = h4_matches[i + 1].start() if i + 1 < len(h4_matches) else sec_end
            block = html[block_start:block_end]

            table_pos = block.find('<table class="table">')
            if table_pos == -1:
                # Real API objects can exist without a field table: methods
                # that "Require no parameters" and types that "hold no
                # information". Keep them with empty annotations.
                description_html = block.strip()
                table_html = None
            else:
                description_html = block[:table_pos].strip()
                table_end = block.find("</table>", table_pos)
                table_html = block[table_pos : table_end + len("</table>")]

            is_method = not obj_name[:1].isupper()
            annotations: list[dict[str, Any]] = []
            if table_html is not None:
                headers, rows = parse_table(table_html)
                has_required_col = any(h.lower() == "required" for h in headers)
                for cells in rows:
                    if has_required_col:
                        if len(cells) < METHOD_CELL_COUNT:
                            continue
                        field_name_html, field_type_html, required_raw, field_desc_html = (
                            cells[0],
                            cells[1],
                            cells[2],
                            cells[3],
                        )
                        required = _html_to_text(required_raw).strip().lower() != "optional"
                    else:
                        if len(cells) < TYPE_CELL_COUNT:
                            continue
                        field_name_html, field_type_html, field_desc_html = (
                            cells[0],
                            cells[1],
                            cells[2],
                        )
                        required = "<em>Optional</em>" not in field_desc_html
                    field_rst = converter.convert(field_desc_html, strip_td=True)
                    annotations.append(
                        {
                            "name": _html_to_text(field_name_html).strip(),
                            "type": _html_to_text(field_type_html).strip(),
                            "required": required,
                            "description": text_converter.convert(field_desc_html, strip_td=True),
                            "html_description": field_desc_html,
                            "rst_description": field_rst + "\n",
                        }
                    )

            child = {
                "anchor": obj_anchor,
                "name": obj_name,
                "description": text_converter.convert(description_html, strip_p=True),
                "html_description": description_html,
                "rst_description": converter.convert(description_html, strip_p=True),
                "annotations": annotations,
                "category": "methods" if is_method else "types",
            }
            children.append(child)

        items.append({"title": title, "anchor": anchor, "children": children})

    return {
        "api": {"version": version, "release_date": release_date},
        "items": items,
    }


def write_schema(schema: dict[str, Any], out_dir: Path) -> None:
    """Write ``schema.json`` and per-object entity caches."""
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "schema.json").write_text(
        json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for group in schema["items"]:
        for child in group["children"]:
            category = child.get("category", "type")
            cache_dir = out_dir / f"{category}s"
            obj_dir = cache_dir / child["name"]
            obj_dir.mkdir(parents=True, exist_ok=True)
            entity = {
                "meta": {},
                "group": {"title": group["title"], "anchor": group["anchor"]},
                "object": child,
            }
            (obj_dir / "entity.json").write_text(
                json.dumps(entity, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )


def _no_redirects(request: urllib.request.Request, _code: int, _headers: dict, response) -> None:
    # The documentation URL is pinned; following redirects to another host
    # would defeat the allowlist above.
    del request, _code, _headers
    raise SystemExit(f"Refusing to follow redirect away from {PAGE_URL}: {response.geturl()}")


class _NoRedirects(urllib.request.HTTPRedirectHandler):
    redirect_request = _no_redirects


def main() -> None:
    """CLI entry point: read the page (cached file or network) and parse it."""
    import argparse
    import urllib.request

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="use a local HTML file instead of downloading",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".api"),
        help="output directory for schema.json and entity caches",
    )
    args = parser.parse_args()

    if args.input is not None:
        html = args.input.read_text(encoding="utf-8")
    else:
        parsed_url = urllib.parse.urlparse(PAGE_URL)
        if parsed_url.scheme != "https" or parsed_url.hostname != "core.telegram.org":
            msg = f"Refusing to fetch a non-official documentation URL: {PAGE_URL}"
            raise SystemExit(msg)
        request = urllib.request.Request(PAGE_URL, headers={"User-Agent": "litegram-api-tool/1.0"})
        opener = urllib.request.build_opener(_NoRedirects())
        with opener.open(request, timeout=60) as response:
            html = response.read().decode("utf-8")

    schema = parse_page(html)
    write_schema(schema, args.output)
    version = schema["api"]["version"]
    n_objects = sum(len(g["children"]) for g in schema["items"])
    n_fields = sum(len(c["annotations"]) for g in schema["items"] for c in g["children"])
    print(f"Parsed Bot API {version}: {n_objects} objects, {n_fields} fields")


if __name__ == "__main__":
    main()
