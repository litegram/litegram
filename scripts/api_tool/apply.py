"""Apply a Bot API schema update to the litegram codebase.

Reads the old and new schemas, then for every API object either generates a
new file (objects absent from the old schema) or patches the existing file in
place (field block + auto-init + docstring, hand-written code preserved).
Finally regenerates package exports and patches ``client/bot.py``.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import replace as dc_replace
from pathlib import Path

from .exports import regen_enums_exports, regen_methods_exports, regen_types_exports
from .families import EnumRegistry
from .gen import Generator, class_name, config_key
from .model import FieldSpec, ObjectSpec, Schema
from .patch import _bot_method_name, patch_bot_file, patch_object_file

REPO_ROOT = Path(__file__).resolve().parents[2]
RUFF = REPO_ROOT / ".venv" / "bin" / "ruff"
MIN_UNION_MEMBERS = 2  # a union needs at least two members

RICH_TEXT_VARIANTS_HINT = "RichText"


def fields_signature(obj: ObjectSpec) -> str:
    """A comparable signature of an object's schema-derived fields."""
    return json.dumps([[a.name, a.type, a.required] for a in obj.annotations], ensure_ascii=False)


def descriptions_signature(obj: ObjectSpec) -> str:
    return json.dumps(
        [obj.rst_description] + [a.rst_description for a in obj.annotations],
        ensure_ascii=False,
    )


def ruff_format(path: Path) -> None:
    subprocess.run(
        [str(RUFF), "format", "--config", str(REPO_ROOT / "pyproject.toml"), str(path)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )


def generate_new_families(generator: Generator, new_schema: Schema, old_schema: Schema) -> list[str]:
    """Generate enum + union files for families introduced by the new schema."""
    registry = EnumRegistry.load()
    created = []
    for base, family in registry.families.items():
        base_obj = new_schema.object(base)
        if base_obj is None:
            continue
        if (
            old_schema.object(base) is not None
            and (REPO_ROOT / "litegram" / "enums" / f"{snake(family.enum_name)}.py").exists()
        ):
            # pre-existing family: leave its enum file untouched
            continue
        enum_path = REPO_ROOT / "litegram" / "enums" / f"{snake(family.enum_name)}.py"
        values: dict[str, str] = {}
        for variant in family.variants:
            vo = new_schema.object(variant)
            if vo is None:
                continue
            fld = vo.field(family.attribute)
            from .families import extract_family_value

            value = extract_family_value(fld.rst_description, family.regexp) if fld else None
            if value:
                values[variant] = value
        if not values:
            continue
        enum_path.parent.mkdir(exist_ok=True)
        enum_path.write_text(generator.render_enum_file(family, values), encoding="utf-8")
        ruff_format(enum_path)
        created.append(str(enum_path))

        # union alias file (skip bases that already have one); the base is
        # always a real object name at this point, so the alias is a string.
        if family.base is None:
            continue
        alias = family.base + "Union"
        union_path = REPO_ROOT / "litegram" / "types" / f"{snake(alias)}.py"
        if alias and not union_path.exists() and _needs_union(new_schema, base):
            union_path.write_text(_render_union(generator, family, values), encoding="utf-8")
            ruff_format(union_path)
            created.append(str(union_path))
    return created


def snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _needs_union(schema: Schema, base: str) -> bool:
    for obj in schema.all_objects():
        for a in obj.annotations:
            if a.type == base or a.type.startswith(f"Array of {base}"):
                return True
    return False


def _render_union(generator: Generator, family, values: dict[str, str]) -> str:
    base = family.base or ""
    alias = generator.resolver.union_alias(base)
    members = family.variants
    if base == "RichText":
        # Recursive union that also accepts plain strings and lists; pydantic
        # needs an explicit discriminator for this shape.
        imports = "\n".join(f"from .{snake(m)} import {m}" for m in members)
        tags = "\n".join(
            f"        | Annotated[{m}, Tag({family.enum_name}.{values[m].upper()})]" for m in members if m in values
        )
        return RICH_TEXT_UNION_TEMPLATE.format(enum=family.enum_name, imports=imports, tags=tags)
    imports = "\n".join(f"from .{snake(m)} import {m}" for m in members)
    expr = " | ".join(members)
    return f"from __future__ import annotations\n\nfrom typing import TypeAlias\n\n{imports}\n\ntype {alias} = {expr}\n"


RICH_TEXT_UNION_TEMPLATE = """from __future__ import annotations

from typing import Annotated, Any

from typing_extensions import TypeAliasType

from pydantic import Discriminator, Tag

from ..enums import {enum}
{imports}


def _rich_text_union_tag(value: Any) -> Any:
    if isinstance(value, str):
        return "str"
    if isinstance(value, (list, tuple)):
        return "list"
    if isinstance(value, dict):
        return value.get("type")
    return getattr(value, "type", None)


RichTextUnion = TypeAliasType(
    "RichTextUnion",
    Annotated[
        Annotated[str, Tag("str")]
        | Annotated[list["RichTextUnion"], Tag("list")]
{tags},
        Discriminator(_rich_text_union_tag),
    ],
)
"""


def sync_curated_unions(generator: Generator, schema: Schema) -> None:
    """Regenerate curated union aliases whose members come from a field's type list.

    Also registers their aliases in the resolver so the source field
    annotations resolve to them. Must run BEFORE the object loop.
    """
    import yaml

    cfg = Path(__file__).resolve().parent / "config" / "curated_unions.yml"
    data = yaml.safe_load(cfg.read_text(encoding="utf-8")) if cfg.exists() else {}
    for alias, spec in (data.get("unions") or {}).items():
        obj = schema.object(spec["object"])
        if obj is None:
            continue
        fld = obj.field(spec["field"])
        if fld is None:
            continue
        t = fld.type
        if t.startswith("Array of "):
            t = t.removeprefix("Array of ")
        members = [p.strip() for p in re.split(r" or |, | and ", t) if p.strip()]
        if len(members) < MIN_UNION_MEMBERS:
            continue
        generator.resolver.union_aliases[alias.removesuffix("Union")] = alias
        generator.resolver.union_by_members[frozenset(members)] = alias
        union_path = REPO_ROOT / "litegram" / "types" / f"{snake(alias)}.py"
        imports = "\n".join(f"from .{snake(m)} import {m}" for m in members)
        union_path.write_text(
            "from __future__ import annotations\n\n"
            "from typing import TypeAlias\n\n"
            f"{imports}\n\n"
            f"type {alias} = " + " | ".join(members) + "\n",
            encoding="utf-8",
        )
        ruff_format(union_path)


def sync_family_unions_and_enums(generator: Generator, new_schema: Schema, old_schema: Schema) -> list[str]:
    """Sync existing family unions/enums with schema-derived variant lists.

    New API versions add variants to existing discriminated families
    (e.g. InputMediaLivePhoto). Variants are derived from the schema itself,
    not the stale enum config lists.
    """
    import yaml

    from .families import extract_family_value

    registry = EnumRegistry.load()
    changed: list[str] = []
    for base, family in registry.families.items():
        base_obj = new_schema.object(base)
        if base_obj is None:
            continue
        variants = [
            name
            for name in new_schema.all_names()
            if name.startswith(base)
            and new_schema.object(name).category == "types"
            and any(a.name == family.attribute and "always '" in a.rst_description for a in new_schema.object(name).annotations)
        ]
        if not variants or set(variants) == set(family.variants):
            continue
        cfg_path = Path(__file__).resolve().parent / "config" / "enums" / f"{family.enum_name}.yml"
        if not cfg_path.exists():
            cfg_path = Path(__file__).resolve().parent / "config" / "enums" / f"{family.enum_name}.yml"
        if cfg_path.exists():
            cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
            cfg["multi_parse"]["entities"] = sorted(variants)
            cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
        values = {}
        for variant in variants:
            vo = new_schema.object(variant)
            fld = vo.field(family.attribute)
            value = extract_family_value(fld.rst_description, family.regexp) if fld else None
            if value:
                values[variant] = value
        if values:
            enum_path = REPO_ROOT / "litegram" / "enums" / f"{snake(family.enum_name)}.py"
            enum_path.write_text(generator.render_enum_file(family, values), encoding="utf-8")
            ruff_format(enum_path)
            changed.append(f"enum {family.enum_name}")
        alias = generator.resolver.union_alias(base)
        union_path = REPO_ROOT / "litegram" / "types" / f"{snake(alias)}.py"
        if union_path.exists():
            union_path.write_text(_render_union(generator, family, values), encoding="utf-8")
            ruff_format(union_path)
            changed.append(f"union {alias}")
    return changed


def main() -> None:  # noqa: PLR0914 — CLI entry point orchestrates the full pipeline
    old_path = REPO_ROOT / ".api" / "schema.json"
    new_path = REPO_ROOT / ".api" / "new" / "schema.json"
    old_schema = Schema.load(old_path)
    new_schema = Schema.load(new_path)
    if old_schema.version == new_schema.version:
        msg = (
            f"Baseline schema is already {old_schema.version}; parse the newer page into "
            f"{new_path} first (make update-api does this) before applying."
        )
        raise SystemExit(msg)
    generator = Generator(new_schema, old_schema)
    registry = EnumRegistry.load()
    # Pre-register union aliases for new families so field annotations
    # resolve to the union alias even before the union files exist.
    for base in registry.families:
        if new_schema.object(base) is None:
            continue
        if base not in generator.resolver.union_aliases:
            generator.resolver.union_aliases[base] = base + "Union"

    # Curated unions must exist in the resolver BEFORE field resolution.
    sync_curated_unions(generator, new_schema)

    added_types: list[str] = []
    added_methods: list[str] = []
    patched: list[str] = []
    unchanged = 0
    generated_blocks: dict[str, str] = {}
    bot_type_names: set[str] = set()

    for obj in new_schema.all_objects():
        old_obj = old_schema.object(obj.name)
        kind_dir = REPO_ROOT / "litegram" / obj.category
        path = kind_dir / f"{obj.module_name}.py"
        if old_obj is None:
            rendered = generator.render_method_file(obj) if obj.category == "methods" else generator.render_type_file(obj)
            path.write_text(rendered, encoding="utf-8")
            ruff_format(path)
            (added_methods if obj.category == "methods" else added_types).append(obj.name)
            if obj.category == "methods":
                block, type_names = _render_bot_block(generator, obj)
                generated_blocks[obj.name] = block
                bot_type_names |= type_names
        elif fields_signature(obj) != fields_signature(old_obj) or descriptions_signature(obj) != descriptions_signature(
            old_obj
        ):
            rendered = generator.render_method_file(obj) if obj.category == "methods" else generator.render_type_file(obj)
            new_src = patch_object_file(path, obj, generator, rendered)
            path.write_text(new_src, encoding="utf-8")
            ruff_format(path)
            patched.append(obj.name)
            if obj.category == "methods":
                block, type_names = _render_bot_block(generator, obj)
                generated_blocks[obj.name] = block
                bot_type_names |= type_names
        else:
            unchanged += 1

    union_enum_files = generate_new_families(generator, new_schema, old_schema)
    union_enum_files += sync_family_unions_and_enums(generator, new_schema, old_schema)
    _regen_extract_enums(generator, new_schema, old_schema)

    # --- bot.py ----------------------------------------------------------------
    bot_path = REPO_ROOT / "litegram" / "client" / "bot.py"
    class_names = {name: config_key(name) for name in generated_blocks}
    bot_src = patch_bot_file(bot_path, generated_blocks, class_names, bot_type_names)
    bot_path.write_text(bot_src, encoding="utf-8")
    ruff_format(bot_path)

    _fixup_renamed_references(generator)

    regen_types_exports(new_schema)
    regen_methods_exports(new_schema)
    regen_enums_exports([])

    # Promote the applied schema to the diff baseline for the next update.
    shutil.copyfile(new_path, REPO_ROOT / ".api" / "schema.json")

    print(
        f"added types: {len(added_types)}, added methods: {len(added_methods)}, "
        f"patched: {len(patched)}, unchanged: {unchanged}, "
        f"enum/union files: {len(union_enum_files)}"
    )
    if added_types:
        print("new types:", ", ".join(sorted(added_types)[:12]), "...")
    if added_methods:
        print("new methods:", ", ".join(sorted(added_methods)))
    if patched:
        print("patched:", ", ".join(sorted(patched)[:12]), "...")


def _fixup_renamed_references(generator: Generator) -> None:
    """Rewrite references to renamed fields in hand-written code.

    When a schema field is renamed (``paid_media_purchased`` ->
    ``purchased_paid_media``), custom code — content-type properties,
    dispatcher observers, middlewares — still references the old name.
    """
    # Explicit code-name fixes: places where the legacy code used a field
    # name that differs from the docs page (and the new schema).
    inverse = {
        "paid_media_purchased": "purchased_paid_media",
    }
    if not inverse:
        return
    targets = [REPO_ROOT / "litegram" / "dispatcher" / "router.py"]
    targets += list((REPO_ROOT / "litegram" / "dispatcher" / "middlewares").glob("*.py"))
    for base_dir in ("types", "utils", "filters"):
        targets.extend((REPO_ROOT / "litegram" / base_dir).glob("*.py"))
    for path in targets:
        lines = path.read_text(encoding="utf-8").split("\n")
        changed = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(("from ", "import ")):
                continue
            new_line = line
            for old, new in inverse.items():
                new_line = re.sub(rf"\.{old}\b", f".{new}", new_line)
                new_line = new_line.replace(f'return "{old}"', f'return "{new}"')
            if new_line != line:
                lines[i] = new_line
                changed = True
        if changed:
            path.write_text("\n".join(lines), encoding="utf-8")


def _regen_extract_enums(generator: Generator, new_schema: Schema, old_schema: Schema) -> None:
    """Regenerate ``extract``-mode enums (e.g. UpdateType) whose base changed.

    Extract enums enumerate the base object's own field names.
    """
    registry = EnumRegistry.load()
    for enum_name, spec in registry.simple_enums.items():
        # Only UpdateType follows the mechanical field->member naming;
        # ContentType and friends are hand-curated taxonomies.
        if enum_name != "UpdateType":
            continue
        if spec.extract_exclude is None or not spec.base:
            continue
        base_new = new_schema.object(spec.base)
        base_old = old_schema.object(spec.base)
        if base_new is None or base_old is None:
            continue
        new_names = [f.name for f in base_new.annotations if f.name not in spec.extract_exclude]
        old_names = [f.name for f in base_old.annotations if f.name not in spec.extract_exclude]
        if new_names == old_names:
            continue
        enum_path = REPO_ROOT / "litegram" / "enums" / f"{snake(enum_name)}.py"
        members = "\n".join(f'    {n.upper()} = "{n}"' for n in new_names)
        desc = (spec.description or "").strip()
        enum_path.write_text(
            "from __future__ import annotations\n\n"
            "from enum import Enum\n\n\n"
            f"class {enum_name}(str, Enum):\n"
            f'    """\n'
            f"    {desc}\n"
            f'    """\n\n'
            f"{members}\n",
            encoding="utf-8",
        )
        ruff_format(enum_path)


def _existing_returning(obj: ObjectSpec) -> str | None:
    """Curated __returning__ of the existing method class, if present."""
    path = REPO_ROOT / "litegram" / obj.category / f"{obj.module_name}.py"
    if not path.exists():
        return None
    m = re.search(r"^    __returning__ = (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return m.group(1) if m else None


def _render_bot_block(generator: Generator, obj: ObjectSpec) -> tuple[str, set[str]]:
    """Render the ``Bot.<method>`` wrapper block for one API method.

    Also returns the ``..types`` names the block references so bot.py's
    TYPE_CHECKING imports can be merged.
    """
    fields = [generator.resolver.render_field(obj, f, None) for f in generator.ordered_fields(obj)]
    method_name = _bot_method_name(obj.name)
    method_class = config_key(obj.name)
    fields.extend(generator._deprecated_extras(obj))
    # python syntax: required parameters must precede optional ones
    ordered = [f for f in fields if f.default_expr is None] + [f for f in fields if f.default_expr is not None]
    params = ["        self,"]
    for f in ordered:
        default = f.default_expr
        ann = f.annotation
        if default is None:
            params.append(f"        {f.name}: {ann},")
        elif default.startswith("Field("):
            params.append(f"        {f.name}: {ann} = None,")
        else:
            params.append(f"        {f.name}: {ann} = {default},")
    params.append("        request_timeout: int | None = None,")
    returning = _existing_returning(obj) or generator._returning_type(obj)
    doc_lines = [obj.rst_description.strip(), "", f"Source: https://core.telegram.org/bots/api#{obj.anchor}"]
    doc_lines.extend(f":param {f.name}: {f.docstring}" for f in fields)
    doc_lines.extend((":param request_timeout: Request timeout", f":return: {obj.rst_description.strip()}"))
    doc = "\n        ".join(doc_lines)
    call_args = "\n".join(f"            {f.name}={f.name}," for f in fields)
    block = (
        f"    async def {method_name}(\n"
        + "\n".join(params)
        + "\n"
        + f"    ) -> {returning}:\n"
        + '        """\n'
        + doc
        + "\n"
        + '        """\n'
        + "\n"
        + f"        call = {method_class}(\n"
        + call_args
        + "\n"
        + "        )\n"
        + "        return await self(call, request_timeout=request_timeout)\n"
    )
    type_names: set[str] = set()
    for f in fields:
        for ident in re.findall(r"\b([A-Z][A-Za-z0-9]*)\b", f.annotation):
            if ident.isupper() or ident in {"Default", "None", "Literal"}:
                continue
            type_names.add(generator.resolver.union_alias(ident) or ident)
    for ident in re.findall(r"\b([A-Z][A-Za-z0-9]*)\b", returning):
        if ident in {"list", "bool"}:
            continue
        type_names.add(generator.resolver.union_alias(ident) or ident)
    return block, type_names


if __name__ == "__main__":
    main()
