"""Generate Sphinx docs pages for new/changed API objects.

Creates ``docs/api/{types,methods}/<name>.rst`` automodule pages and updates
the ``index.rst`` toctrees of both sections.
"""

from __future__ import annotations

import re
from pathlib import Path

from .gen import REPO_ROOT
from .model import Schema, snake_case

PAGE_TEMPLATE = """{underline}
{name}
{underline}


.. automodule:: litegram.{category}.{module}
    :members:
    :member-order: bysource
    :undoc-members: True
    :exclude-members: model_config,model_fields
"""


def render_page(name: str, category: str) -> str:
    module = snake_case(name)
    underline = "#" * max(len(name), 5)
    return PAGE_TEMPLATE.format(underline=underline, name=name, category=category, module=module)


def sync_docs(schema: Schema) -> int:
    """Create rst pages for new objects and sync the toctrees."""
    created = 0
    for category in ("types", "methods"):
        out_dir = REPO_ROOT / "docs" / "api" / category
        objects = sorted(
            getattr(schema, category),
            key=lambda o: snake_case(o.name),
        )
        for obj in objects:
            page = out_dir / f"{snake_case(obj.name)}.rst"
            if not page.exists():
                page.write_text(render_page(obj.name, category), encoding="utf-8")
                created += 1
        # sync toctree: list every page in the section
        index = out_dir / "index.rst"
        if index.exists():
            text = index.read_text(encoding="utf-8")
            m = re.search(r"\.\. toctree::\n(?:    .*\n)*\n", text)
            if m:
                body = m.group(0)
                present = set(re.findall(r"^    ([a-z_0-9]+)$", body, re.MULTILINE))
                wanted = {snake_case(o.name) for o in objects}
                missing = sorted(wanted - present)
                if missing:
                    # insert missing entries into the alphabetical list
                    all_entries = sorted(present | wanted)
                    entries_text = "".join(f"    {name}\n" for name in all_entries)
                    new_body = re.sub(
                        r"(\.\. toctree::\n(?:    .*\n)*\n)(?:.*?)(?=\n\S|\Z)",
                        lambda mm, entries_text=entries_text: mm.group(1) + entries_text,
                        body,
                        flags=re.DOTALL,
                    )
                    text = text.replace(body, new_body, 1)
                    index.write_text(text, encoding="utf-8")
    return created


def main() -> None:
    schema = Schema.load(REPO_ROOT / ".api" / "schema.json")
    created = sync_docs(schema)
    print(f"docs pages created: {created}")


if __name__ == "__main__":
    main()
