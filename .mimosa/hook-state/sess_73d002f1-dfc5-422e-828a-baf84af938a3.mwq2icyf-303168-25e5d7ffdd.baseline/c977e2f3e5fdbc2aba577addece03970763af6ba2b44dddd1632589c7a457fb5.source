"""Sync ``Dispatcher``/``Router`` event observers with Update fields.

The router declares one ``TelegramEventObserver`` per update type with a
hardcoded ``observers`` mapping. This script adds observers for update types
that appeared in a newer schema and renames drifted ones.

Run after ``apply``:
    python3 -m scripts.api_tool.sync_router
"""

from __future__ import annotations

import re
from pathlib import Path

from .gen import REPO_ROOT
from .model import Schema

ROUTER_PATH = REPO_ROOT / "litegram" / "dispatcher" / "router.py"


def sync_router(schema: Schema) -> list[str]:  # noqa: PLR0914 — sync tracks many local accumulators
    update = schema.object("Update")
    field_names = [f.name for f in update.annotations if f.name != "update_id"]

    src = ROUTER_PATH.read_text(encoding="utf-8")
    changed = []

    decl_re = re.compile(
        r"        self\.([a-z_0-9]+) = TelegramEventObserver\(\n"
        r"            router=self,\n"
        r"            event_name=\"([a-z_0-9]+)\",\n"
        r"        \)\n"
    )
    decls = {m.group(2): m.group(1) for m in decl_re.finditer(src)}
    single_re = re.compile(r"        self\.([a-z_0-9]+) = TelegramEventObserver\(router=self, event_name=\"([a-z_0-9]+)\"\)\n")
    for m in single_re.finditer(src):
        decls[m.group(2)] = m.group(1)

    m = re.search(
        r"        self\.observers: dict\[str, TelegramEventObserver\] = \{\n(.*?)\n        \}",
        src,
        re.DOTALL,
    )
    if m is None:
        raise RuntimeError("observers dict not found in router.py")
    existing_keys = set(re.findall(r'"([a-z_0-9]+)":', m.group(1)))

    decls_by_attr = {attr: event for event, attr in decls.items()}
    additions: list[str] = []
    for name in field_names:
        if name in existing_keys:
            continue
        changed.append(f"+ observer {name}")
        if name in decls_by_attr:
            # Observer exists under a drifted event name: fix the event name.
            drifted = decls_by_attr[name]
            src = src.replace(f'event_name="{drifted}",', f'event_name="{name}",', 1)
            attr = name
        elif name in decls:
            attr = decls[name]
        else:
            attr = name
            decl = f'        self.{name} = TelegramEventObserver(router=self, event_name="{name}")\n'
            anchor = '        self.errors = self.error = TelegramEventObserver(router=self, event_name="error")'
            src = src.replace(anchor, decl + "\n" + anchor, 1)
        additions.append(f'            "{name}": self.{attr},')

    if additions:
        block = m.group(1).rstrip("\n")
        src = src.replace(
            m.group(0),
            m.group(0).replace(block, block + "\n" + "\n".join(additions)),
            1,
        )
        ROUTER_PATH.write_text(src, encoding="utf-8")
    return changed


def main() -> None:
    schema = Schema.load(REPO_ROOT / ".api" / "schema.json")
    changed = sync_router(schema)
    for line in changed:
        print(line)
    print(f"router observers: {len(changed)} added")


if __name__ == "__main__":
    main()
