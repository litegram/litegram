"""Delta patching for existing generated files.

Unlike :mod:`api_tool.gen` (which renders whole files for new objects), the
patcher rewrites only the schema-derived parts of an existing file — the
class docstring, the field block and the auto-generated ``TYPE_CHECKING``
``__init__`` — and leaves all hand-written code (helper methods, custom
imports, custom properties) untouched.
"""

from __future__ import annotations

import re
from pathlib import Path  # noqa: TC003 — used at runtime

from .gen import Generator  # noqa: TC001 — used at runtime
from .model import ObjectSpec  # noqa: TC001 — used at runtime

AUTO_INIT_START = (
    "    if TYPE_CHECKING:\n"
    "        # DO NOT EDIT MANUALLY!!!\n"
    "        # This section was auto-generated via the litegram api tool\n"
)

CUSTOM_SECTION_RE = re.compile(r"^    (?:@|def |async def |if TYPE_CHECKING:)", re.MULTILINE)

METHOD_DEF_RE = re.compile(r"^    async def ([a-z_0-9]+)\(\n", re.MULTILINE)


def _find_class_docstring(src: str, class_name_str: str) -> tuple[int, int] | None:
    """Locate the ``class X(...):`` docstring span (start, end) offsets."""
    class_re = re.compile(
        rf"^class {re.escape(class_name_str)}\([^)]*\):\n(    \"\"\"\n.*?\n    \"\"\"\n)",
        re.DOTALL | re.MULTILINE,
    )
    m = class_re.search(src)
    if m is None:
        return None
    return m.start(1), m.end(1)


def _find_auto_init(src: str) -> tuple[int, int] | None:
    """Locate the auto-generated TYPE_CHECKING __init__ block."""
    start = src.find(AUTO_INIT_START)
    if start == -1:
        return None
    # The block ends at the end of the super().__init__ call: find the
    # closing paren of the call that follows "super().__init__(".
    call_pos = src.find("super().__init__(", start)
    if call_pos == -1:
        # Zero-field block: ends at the intro's end (should not happen).
        return start, start + len(AUTO_INIT_START)
    # Scan from after the "super().__init__(" prefix: the "super()" part
    # contains a balanced paren pair that would otherwise end the scan early.
    scan_from = call_pos + len("super().__init__(")
    depth = 1
    for i in range(scan_from, len(src)):
        ch = src[i]
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                end = i + 1
                # swallow the trailing newline
                if end < len(src) and src[end] == "\n":
                    end += 1
                return start, end
    return start, len(src)


def _find_field_block(src: str, docstring_end: int) -> tuple[int, int]:
    """Field block spans from the docstring end to the next section."""
    boundaries = []
    auto = _find_auto_init(src)
    if auto is not None:
        boundaries.append(auto[0])
    m = CUSTOM_SECTION_RE.search(src, docstring_end)
    if m is not None:
        boundaries.append(m.start())
    end = min(boundaries) if boundaries else len(src)
    return docstring_end, end


def patch_object_file(  # noqa: PLR0914 — patch orchestration tracks many spans
    path: Path,
    obj: ObjectSpec,
    generator: Generator,
    rendered: str,
) -> str:
    """Patch a single generated file in place, return the new source."""
    src = path.read_text(encoding="utf-8")

    class_name_str = obj.name[:1].upper() + obj.name[1:] if obj.category == "methods" else obj.name

    # --- class docstring ----------------------------------------------------
    doc_span = _find_class_docstring(src, class_name_str)
    new_doc = _extract_docstring(rendered, class_name_str)
    if doc_span is not None and new_doc is not None:
        src = src[: doc_span[0]] + new_doc + src[doc_span[1] :]

    # --- field block ---------------------------------------------------------
    doc_span = _find_class_docstring(src, class_name_str)
    if doc_span is not None:
        fb_start, fb_end = _find_field_block(src, doc_span[1])
        new_fields = _extract_field_block(rendered, class_name_str)
        if obj.category == "methods":
            # Preserve the curated __returning__ / __api_method__ lines.
            kept = [
                line
                for line in src[fb_start:fb_end].split("\n")
                if line.startswith("    __returning__") or line.startswith("    __api_method__")
            ]
            generated = [
                line
                for line in new_fields.split("\n")
                if not line.startswith("    __returning__") and not line.startswith("    __api_method__")
            ]
            new_fields = "\n".join(kept + generated)
        src = src[:fb_start] + new_fields + src[fb_end:]

    # --- auto-init block -------------------------------------------------------
    auto_span = _find_auto_init(src)
    new_auto = _extract_auto_init(rendered)
    if auto_span is not None and new_auto is not None:
        src = src[: auto_span[0]] + new_auto + src[auto_span[1] :]
    elif auto_span is None and new_auto is not None:
        # no auto-init present: insert it after the field block
        doc_span = _find_class_docstring(src, class_name_str)
        if doc_span is not None:
            fb_start, fb_end = _find_field_block(src, doc_span[1])
            src = src[:fb_end] + "\n" + new_auto + src[fb_end:]

    src = _merge_imports(src, rendered, obj)
    if obj.category == "methods":
        src = _dedupe_single_type_imports(src)
    return src


def _extract_docstring(rendered: str, class_name_str: str) -> str | None:
    m = re.search(
        rf"class {re.escape(class_name_str)}\([^)]*\):\n(    \"\"\"\n.*?\n    \"\"\"\n)",
        rendered,
        re.DOTALL,
    )
    return m.group(1) if m else None


def _extract_field_block(rendered: str, class_name_str: str) -> str:
    m = re.search(
        rf"class {re.escape(class_name_str)}\([^)]*\):\n    \"\"\"\n.*?\n    \"\"\"\n(.*?)(?=\n    if TYPE_CHECKING:\n|\Z)",
        rendered,
        re.DOTALL,
    )
    if m is None:
        return ""
    block = m.group(1)
    return block.rstrip("\n") + "\n"


def _extract_auto_init(rendered: str) -> str | None:
    start = rendered.find(AUTO_INIT_START)
    if start == -1:
        return None
    span = _find_auto_init(rendered)
    if span is None:
        return None
    return rendered[start : span[1]]


INLINE_IMPORT_LIMIT = 4  # switch to parenthesised form above this count


def _dedupe_single_type_imports(src: str) -> str:
    """Remove redundant ``from ..types.x import X`` duplicates of main imports."""
    main_names = set(re.findall(r"^    ([A-Za-z_0-9]+),$", src, re.MULTILINE))
    for names_line in re.findall(r"^from \.\.types import ([A-Za-z_0-9, ]+)$", src, re.MULTILINE):
        main_names.update(n.strip() for n in names_line.split(",") if n.strip())
    for names_line in re.findall(r"^    from \.\.types import ([A-Za-z_0-9, ]+)$", src, re.MULTILINE):
        main_names.update(n.strip() for n in names_line.split(",") if n.strip())
    for match in re.findall(r"^    from \.\.types\.[a-z_0-9]+ import ([A-Za-z_0-9]+)$", src, re.MULTILINE):
        if match in main_names:
            src = re.sub(
                rf"^    from \.\.types\.[a-z_0-9]+ import {re.escape(match)}\n",
                "",
                src,
                count=1,
                flags=re.MULTILINE,
            )
    return src


def _merge_imports(src: str, rendered: str, obj: ObjectSpec) -> str:  # noqa: PLR0914 — merge logic tracks many spans
    """Add missing imports that the new fields require.

    Type files: single-line ``from .module import Name`` entries inside the
    module-level TYPE_CHECKING block are inserted at sorted positions; any
    other content (e.g. nested ``from ..methods import (...)`` blocks with
    hand-written shortcut imports) is left untouched.
    Method files: names are merged into the ``from ..types import (...)``
    list.
    """
    if obj.category == "methods":
        # collect wanted names from either parenthesised or single-line forms
        wanted: set[str] = set()
        if re.search(r"^from \.\.types import \(", rendered, re.MULTILINE):
            m_r = re.search(r"^from \.\.types import \(\n(.*?)\n\)", rendered, re.DOTALL | re.MULTILINE)
            if m_r:
                wanted |= set(re.findall(r"    ([A-Za-z_0-9]+),", m_r.group(1)))
        else:
            m_r = re.search(r"^from \.\.types import (.+)$", rendered, re.MULTILINE)
            if m_r:
                wanted |= {n.strip() for n in m_r.group(1).split(",") if n.strip()}
        if not wanted:
            return src
        if re.search(r"^from \.\.types import \(", src, re.MULTILINE):
            m = re.search(r"^from \.\.types import \(\n(.*?)\n\)", src, re.DOTALL | re.MULTILINE)
            if m is None:
                return src
            present = set(re.findall(r"    ([A-Za-z_0-9]+),", m.group(1)))
            missing = wanted - present
            if not missing:
                return src
            merged = sorted(present | missing)
            inner = "".join(f"    {name},\n" for name in merged)
            return src.replace(m.group(0), f"from ..types import (\n{inner})", 1)
        # single-line import in the source file
        m = re.search(r"^from \.\.types import (.+)$", src, re.MULTILINE)
        if m is None:
            # The ..types import may live inside a TYPE_CHECKING block
            # (some files use that convention when __returning__ is scalar).
            m_tc = re.search(r"^    from \.\.types import (.+)$", src, re.MULTILINE)
            if m_tc is None:
                # No ..types import anywhere in the file: create a top-level one.
                if not re.search(r"^from \.\.types import \(", src, re.MULTILINE):
                    if wanted:
                        merged = sorted(wanted)
                        inner = "".join(f"    {name},\n" for name in merged)
                        anchor = "from .base import TelegramMethod"
                        new_import = f"from ..types import (\n{inner})\n{anchor}"
                        return src.replace(anchor, new_import, 1)
                    return src
                m_tc_paren = re.search(r"^    from \.\.types import \(\n(.*?)\n    \)", src, re.DOTALL | re.MULTILINE)
                if m_tc_paren is None:
                    return src
                present = set(re.findall(r"        ([A-Za-z_0-9]+),", m_tc_paren.group(1)))
                missing = wanted - present
                if not missing:
                    return src
                merged = sorted(present | missing)
                inner = "".join(f"        {name},\n" for name in merged)
                return src.replace(
                    m_tc_paren.group(0),
                    f"    from ..types import (\n{inner})",
                    1,
                )
            present = {n.strip() for n in m_tc.group(1).split(",") if n.strip()}
            missing = wanted - present
            if not missing:
                return src
            merged = sorted(present | missing)
            if len(merged) > INLINE_IMPORT_LIMIT:
                inner = "".join(f"        {name},\n" for name in merged)
                return src.replace(m_tc.group(0), f"    from ..types import (\n{inner})", 1)
            return src.replace(m_tc.group(0), "    from ..types import " + ", ".join(merged), 1)
        present = {n.strip() for n in m.group(1).split(",") if n.strip()}
        missing = wanted - present
        if not missing:
            return src
        merged = sorted(present | missing)
        if len(merged) > INLINE_IMPORT_LIMIT:
            inner = "".join(f"    {name},\n" for name in merged)
            return src.replace(m.group(0), f"from ..types import (\n{inner})", 1)
        return src.replace(m.group(0), "from ..types import " + ", ".join(merged), 1)

    # types file: insert missing single-line refs into the TYPE_CHECKING block
    rendered_pairs = set(
        re.findall(
            r"^    from \.([a-z_0-9]+) import ([A-Za-z_0-9]+)$",
            rendered,
            re.MULTILINE,
        )
    )
    src_tc = re.search(r"^if TYPE_CHECKING:\n", src, re.MULTILINE)
    if src_tc is None or not rendered_pairs:
        return src
    block_start = src_tc.end()
    # find the end of the TYPE_CHECKING block: first non-indented line
    block_end = block_start
    while block_end < len(src):
        line_end = src.find("\n", block_end)
        if line_end == -1:
            line_end = len(src)
        line = src[block_end:line_end]
        if line and not line.startswith(" "):
            break
        block_end = line_end + 1
    block_text = src[block_start:block_end]
    lines = block_text.split("\n")
    SORTABLE = re.compile(r"^    from \.([a-z_0-9]+) import ([A-Za-z_0-9]+)$")
    # locate the contiguous run of sortable single-line imports
    runs = []
    i = 0
    while i < len(lines):
        if SORTABLE.match(lines[i]):
            j = i
            while j < len(lines) and SORTABLE.match(lines[j]):
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    if not runs:
        return src
    # merge into the longest run
    run_start, run_end = max(runs, key=lambda r: r[1] - r[0])
    present_pairs = {SORTABLE.match(lines[k]).groups() for k in range(run_start, run_end)}
    missing_pairs = rendered_pairs - present_pairs
    if not missing_pairs:
        return src
    merged = sorted(present_pairs | missing_pairs)
    merged_lines = [f"    from .{module} import {name}" for module, name in merged]
    lines[run_start:run_end] = merged_lines
    new_block = "\n".join(lines)
    return src[:block_start] + new_block + src[block_end:]


def _module_of(tc_block: str, name: str) -> str:
    m = re.search(rf"^    from \.([a-z_0-9]+) import {re.escape(name)}$", tc_block, re.MULTILINE)
    return m.group(1) if m else "unknown"


def patch_bot_file(
    bot_path: Path,
    methods: dict[str, str],
    class_names: dict[str, str],
    type_import_names: set[str] | None = None,
) -> str:
    """Patch ``litegram/client/bot.py``.

    ``methods`` maps api method name -> rendered ``async def`` block for
    NEW or CHANGED methods; ``class_names`` maps api name -> import class.
    """
    src = bot_path.read_text(encoding="utf-8")
    for api_name, block in methods.items():
        pattern = re.compile(
            rf"    async def {re.escape(_bot_method_name(api_name))}\(\n"
            rf".*?return await self\(call, request_timeout=request_timeout\)\n",
            re.DOTALL | re.MULTILINE,
        )
        if pattern.search(src):
            src = pattern.sub(block.replace("\\", "\\\\"), src, count=1)
        else:
            # Append new methods at the end of the class (file end).
            if not src.endswith("\n"):
                src += "\n"
            src += "\n" + block
    # merge method-class imports
    m = re.search(r"^from \.\.methods import \(\n(.*?)\n\)", src, re.DOTALL | re.MULTILINE)
    if m is not None:
        present = set(re.findall(r"    ([A-Za-z_0-9]+),", m.group(1)))
        missing = sorted(set(class_names.values()) - present)
        if missing:
            merged = sorted(present | set(missing))
            inner = "".join(f"    {name},\n" for name in merged)
            src = src.replace(m.group(0), f"from ..methods import (\n{inner})", 1)
    # merge TYPE_CHECKING ..types imports referenced by the blocks
    if type_import_names:
        m = re.search(r"^    from \.\.types import \(\n(.*?)\n    \)", src, re.DOTALL | re.MULTILINE)
        if m is not None:
            present = set(re.findall(r"        ([A-Za-z_0-9]+),", m.group(1)))
            missing = sorted(type_import_names - present)
            if missing:
                merged = sorted(present | set(missing))
                inner = "".join(f"        {name},\n" for name in merged)
                src = src.replace(m.group(0), f"    from ..types import (\n{inner})", 1)
    return src


def _bot_method_name(api_name: str) -> str:
    """sendMessage -> send_message; addStickerToSet -> add_sticker_to_set."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", api_name).lower()
