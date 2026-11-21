"""Regenerate package exports (``__init__.py``) for types, methods and enums.

Existing files are patched additively: new ``from .module import Name`` lines
and ``__all__`` entries are inserted at their sorted positions; everything
else (including the lazy forward-ref loading loops) is preserved.
"""

from __future__ import annotations

import re
from pathlib import Path

from .gen import REPO_ROOT, class_name, config_key
from .model import Schema, snake_case

IMPORT_RE = re.compile(r"^from \.([a-z_0-9]+) import ([A-Za-z_0-9, ]+)$", re.MULTILINE)
SINGLE_LINE_MULTI_RE = re.compile(r"^from \.([a-z_0-9]+) import [A-Za-z_0-9]+(?:, [A-Za-z_0-9]+)+$", re.MULTILINE)
ALL_ENTRY_RE = re.compile(r'^    "([A-Za-z_0-9]+)",$', re.MULTILINE)


def _merge_name_imports(text: str, wanted: dict[str, str]) -> str:  # noqa: PLR0914 — merge logic spans many local tracking vars
    """Merge ``module -> name`` imports at their sorted positions.

    Handles both single-line and parenthesised multi-name imports; missing
    modules are inserted relative to the sorted module order of all existing
    import lines in the file.
    """
    single_re = re.compile(r"^from \.([a-z_0-9]+) import ([A-Za-z_0-9]+)$", re.MULTILINE)
    paren_re = re.compile(r"^from \.([a-z_0-9]+) import \(", re.MULTILINE)
    multi_re = re.compile(r"^from \.([a-z_0-9]+) import [A-Za-z_0-9]+(?:, [A-Za-z_0-9]+)+$", re.MULTILINE)
    multi_modules = {m.group(1) for m in multi_re.finditer(text)}
    for module in sorted(set(wanted) & multi_modules):
        m = re.search(rf"^from \.{module} import (.+)$", text, re.MULTILINE)
        if m is None:
            continue
        present_names = {n.strip() for n in m.group(1).split(",") if n.strip()}
        add = [n for n in wanted[module].split(", ") if n not in present_names]
        if not add:
            continue
        merged = sorted(present_names | set(add))
        text = text.replace(m.group(0), f"from .{module} import " + ", ".join(merged), 1)
    present_modules = set(single_re.findall.__self__ if False else [])  # noqa: F841
    existing_single = {m.group(1): m.group(2) for m in single_re.finditer(text)}
    paren_modules = {m.group(1) for m in paren_re.finditer(text)}

    # merge names into parenthesised blocks first
    for module in sorted(set(wanted) & paren_modules):
        m = re.search(rf"^from \.{module} import \(\n(.*?)\n\)", text, re.DOTALL | re.MULTILINE)
        if m is None:
            continue
        present_names = set(re.findall(r"^    ([A-Za-z_0-9]+),$", m.group(1), re.MULTILINE))
        add = [n for n in wanted[module].split(", ") if n not in present_names]
        if not add:
            continue
        merged = sorted(present_names | set(add))
        if len(merged) == 1:
            replacement = f"from .{module} import {merged[0]}"
        else:
            inner = "".join(f"    {n},\n" for n in merged)
            replacement = f"from .{module} import (\n{inner})"
        text = text.replace(m.group(0), replacement, 1)

    missing = {
        m: n for m, n in wanted.items() if m not in existing_single and m not in paren_modules and m not in multi_modules
    }
    if not missing:
        return text
    # Insert each missing import before the first single-line import whose
    # module sorts after it (falling back to appending after the last one).
    lines = text.split("\n")
    for module, name in sorted(missing.items()):
        new_line = f"from .{module} import {name}"
        inserted = False
        for i, line in enumerate(lines):
            m = single_re.match(line)
            if m and m.group(1) > module:
                lines.insert(i, new_line)
                inserted = True
                break
        if not inserted:
            # append after the last single-line import (or the last paren block)
            last_idx = None
            for i, line in enumerate(lines):
                if single_re.match(line) or paren_re.match(line):
                    last_idx = i
            if last_idx is None:
                lines.append(new_line)
            else:
                lines.insert(last_idx + 1, new_line)
    return "\n".join(lines)


def _merge_all_entries(text: str, wanted: set[str]) -> str:
    present = set(ALL_ENTRY_RE.findall(text))
    missing = sorted(wanted - present)
    if not missing:
        return text
    all_entries = sorted(present | set(missing))
    # Rebuild the __all__ block wholesale from the sorted entries.
    block_re = re.compile(r"__all__ = \(\n(.*?)\n\)", re.DOTALL)
    m = block_re.search(text)
    if m is None:
        return text
    inner = "".join(f'    "{n}",\n' for n in all_entries)
    return text[: m.start()] + "__all__ = (\n" + inner + ")" + text[m.end() :]


def regen_types_exports(schema: Schema) -> None:
    path = REPO_ROOT / "litegram" / "types" / "__init__.py"
    text = path.read_text(encoding="utf-8")
    wanted = {}
    all_names = set()
    for t in schema.types:
        if not t.name[:1].isupper():
            continue
        wanted[snake_case(t.name)] = t.name
        all_names.add(t.name)
    for path_u in (REPO_ROOT / "litegram" / "types").glob("*_union.py"):
        name = class_name(path_u.stem)
        wanted[path_u.stem] = name
        all_names.add(name)
    wanted.setdefault("custom", "DateTime")
    wanted.setdefault("input_file", "InputFile")
    all_names.update(("DateTime", "InputFile", "UNSET_PARSE_MODE"))
    text = _merge_name_imports(text, wanted)
    text = _merge_all_entries(text, all_names)
    path.write_text(text, encoding="utf-8")


def regen_methods_exports(schema: Schema) -> None:
    path = REPO_ROOT / "litegram" / "methods" / "__init__.py"
    text = path.read_text(encoding="utf-8")
    wanted = {snake_case(m.name): config_key(m.name) for m in schema.methods}
    wanted["base"] = "Request, Response, TelegramMethod"
    all_names = {config_key(m.name) for m in schema.methods} | {
        "Request",
        "Response",
        "TelegramMethod",
    }
    # base import is not module->single-name; handle separately
    del wanted["base"]
    text = _merge_name_imports(text, wanted)
    text = _merge_all_entries(text, all_names)
    path.write_text(text, encoding="utf-8")


def regen_enums_exports(new_enum_names: list[str]) -> None:
    path = REPO_ROOT / "litegram" / "enums" / "__init__.py"
    text = path.read_text(encoding="utf-8")
    wanted = {}
    for path_e in sorted((REPO_ROOT / "litegram" / "enums").glob("*.py")):
        if path_e.stem == "__init__":
            continue
        m = re.search(r"^class (\w+)\(", path_e.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            wanted[path_e.stem] = m.group(1)
    text = _merge_name_imports(text, wanted)
    text = _merge_all_entries(text, set(wanted.values()))
    path.write_text(text, encoding="utf-8")
