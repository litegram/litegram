"""Bootstrap curated codegen configs from the existing generated code.

The generated API layer carries curation that is not present on the docs
page: ``Default(...)`` sentinels, deprecated fields and explicit type
overrides (``DateTime`` timestamps, union aliases, ``Field(...)`` markers).
This script walks the existing ``litegram/{types,methods}`` files and dumps
the curated data into ``config/`` YAML files, which then drive generation.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from .gen import config_key
from .model import Schema

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_VALUE_RE = re.compile(r'Default\("(?P<name>[a-z_0-9]+)"\)')


def deprecated_pattern(field_name: str) -> re.Pattern[str]:
    """Regex matching a deprecated field with its docstring deprecation block."""
    name = re.escape(field_name)
    return re.compile(
        rf'^    {name}: .*\n    """.*?\.\. deprecated:: API:(?P<version>[\d.]+)\n'
        r"   (?P<url>\S+?)\x22{3}",
        re.DOTALL | re.MULTILINE,
    )


def bare_deprecated_pattern(field_name: str) -> re.Pattern[str]:
    """Regex matching a deprecated field without a deprecation docstring."""
    name = re.escape(field_name)
    return re.compile(
        rf'^    {name}: .*json_schema_extra=\{{"deprecated": True\}}\n    """',
        re.MULTILINE,
    )


def field_defs(src: str, field_name: str) -> list[str]:
    """All annotation lines of a field in a generated file."""
    return re.findall(rf"^    {re.escape(field_name)}: (.+)$", src, re.MULTILINE)


def extract_deprecated(src: str, field_name: str) -> dict[str, Any] | None:
    """Extract deprecation metadata from a field definition, if any."""
    m = deprecated_pattern(field_name).search(src)
    if m:
        return {"version": m.group("version"), "url": m.group("url")}
    if bare_deprecated_pattern(field_name).search(src):
        return {}
    return None


def scan_code_deprecations() -> dict[str, dict[str, Any]]:
    """Scan all generated files for deprecated fields.

    Deprecated fields are absent from the docs page (Telegram dropped them
    from the tables), so they can only be discovered from the code itself.
    The annotation and docstring are captured alongside the deprecation
    metadata so the generator can re-emit these fields verbatim.
    """
    deprecations: dict[str, dict[str, Any]] = defaultdict(dict)
    pattern = re.compile(
        r"^    ([a-z_0-9]+): ([^=]+?) = Field\(None, json_schema_extra=\{\"deprecated\": True\}\)\n"
        r'    """(?P<doc>.*?)"""',
        re.MULTILINE | re.DOTALL,
    )
    for category in ("types", "methods"):
        for path in sorted((REPO_ROOT / "litegram" / category).glob("*.py")):
            if path.stem == "__init__":
                continue
            src = path.read_text(encoding="utf-8")
            class_name = snake_case_to_class(path.stem)
            for m in pattern.finditer(src):
                field_name, annotation, doc = m.groups()
                doc = doc.strip()
                dep = extract_deprecated(src, field_name) or {}
                dep["annotation"] = annotation.strip()
                dep["docstring"] = doc.split("\n\n.. deprecated::")[0].strip()
                deprecations[class_name][field_name] = dep
    return deprecations


def snake_case_to_class(module: str) -> str:
    return "".join(part.capitalize() for part in module.split("_"))


def main() -> None:
    schema = Schema.load(REPO_ROOT / ".api" / "schema.json")
    config_dir = Path(__file__).resolve().parent / "config"
    config_dir.mkdir(exist_ok=True)

    defaults: dict[str, dict[str, str]] = defaultdict(dict)
    type_overrides: dict[str, dict[str, str]] = defaultdict(dict)
    curated_defaults: dict[str, dict[str, str]] = defaultdict(dict)

    for obj in schema.all_objects():
        path = REPO_ROOT / "litegram" / obj.category / f"{obj.module_name}.py"
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8")
        for ann in obj.annotations:
            defs = field_defs(src, ann.name)
            if not defs:
                continue
            body = defs[0]
            if "Default(" in body:
                m = DEFAULT_VALUE_RE.search(body)
                if m:
                    defaults[config_key(obj.name)][ann.name] = m.group("name")
            # Exact python annotation (without default value) — the source of
            # truth for the type resolver on regeneration.
            type_overrides[config_key(obj.name)][ann.name] = body.split(" = ")[0].strip()
            if " = " in body:
                curated_defaults[config_key(obj.name)][ann.name] = body.split(" = ", 1)[1].strip()

    deprecations = scan_code_deprecations()

    # Field order as present in the code (historical curation, differs
    # from the docs page order for many objects).
    field_order: dict[str, list[str]] = {}
    for obj in schema.all_objects():
        path = REPO_ROOT / "litegram" / obj.category / f"{obj.module_name}.py"
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8")
        positions = []
        for ann in obj.annotations:
            m = re.search(rf"^    {re.escape(ann.name)}: ", src, re.MULTILINE)
            if m:
                positions.append((m.start(), ann.name))
        if positions:
            order = [name for _, name in sorted(positions)]
            if order != [a.name for a in obj.annotations]:
                field_order[config_key(obj.name)] = order

    def clean(d: dict[str, Any], sort: bool = True) -> dict[str, Any]:
        if sort:
            return {k: v for k, v in sorted(d.items()) if v}
        return {k: v for k, v in d.items() if v}

    (config_dir / "defaults.yml").write_text(
        yaml.safe_dump(clean(defaults), sort_keys=True, allow_unicode=True),
        encoding="utf-8",
    )
    (config_dir / "deprecations.yml").write_text(
        yaml.safe_dump(clean(deprecations, sort=False), sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (config_dir / "type_overrides.yml").write_text(
        yaml.safe_dump(clean(type_overrides), sort_keys=True, allow_unicode=True),
        encoding="utf-8",
    )
    (config_dir / "curated_defaults.yml").write_text(
        yaml.safe_dump(clean(curated_defaults), sort_keys=True, allow_unicode=True),
        encoding="utf-8",
    )
    (config_dir / "field_order.yml").write_text(
        yaml.safe_dump(dict(sorted(field_order.items())), sort_keys=True, allow_unicode=True),
        encoding="utf-8",
    )
    print(
        f"defaults: {len(defaults)} objects, "
        f"deprecations: {sum(len(v) for v in deprecations.values())} fields, "
        f"type_overrides: {sum(len(v) for v in type_overrides.values())} fields, "
        f"field_order: {len(field_order)} objects"
    )


if __name__ == "__main__":
    main()
