"""Generate Sphinx docs pages for new/changed API objects.

Creates ``docs/api/{types,methods}/<name>.rst`` automodule pages and updates
the ``index.rst`` toctrees of both sections.
"""

from __future__ import annotations

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


def render_index(category: str, pages: list[str]) -> str:
    title = category.capitalize()
    heading = f"Available {category}"
    entries = "\n".join(f"    {page}" for page in sorted(pages))
    return (
        f"{'#' * len(title)}\n{title}\n{'#' * len(title)}\n\n"
        f"Here is list of all available API {category}:\n\n\n"
        f"{heading}\n{'=' * len(heading)}\n\n"
        f".. toctree::\n    :maxdepth: 1\n\n{entries}\n"
    )


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
        # A single deterministic toctree avoids duplicate pages in the general
        # list and the old manually maintained category lists.
        pages = [page.stem for page in out_dir.glob("*.rst") if page.stem != "index"]
        (out_dir / "index.rst").write_text(render_index(category, pages), encoding="utf-8")
    return created


def main() -> None:
    schema = Schema.load(REPO_ROOT / ".api" / "schema.json")
    created = sync_docs(schema)
    print(f"docs pages created: {created}")


if __name__ == "__main__":
    main()
