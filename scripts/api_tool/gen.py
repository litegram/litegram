"""Code generation for the litegram API layer.

Renders ``litegram/{types,methods}/<name>.py``, union aliases and enums from
the parsed schema. Generation is delta-aware: existing files get their field
blocks and auto-generated ``TYPE_CHECKING`` signatures rewritten while
hand-written code is preserved; new objects produce whole new files.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field as dc_field
from pathlib import Path
from typing import Any

import yaml

from .families import EnumRegistry, Family, extract_family_value
from .model import FieldSpec, ObjectSpec, Schema, snake_case

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = Path(__file__).resolve().parent / "config"

AUTO_INIT_INTRO = (
    "    if TYPE_CHECKING:\n"
    "        # DO NOT EDIT MANUALLY!!!\n"
    "        # This section was auto-generated via `butcher`\n"
    "\n"
    "        def __init__(\n"
    "            __pydantic__self__,\n"
    "            *,\n"
)
AUTO_INIT_OUTRO = (
    "            **__pydantic_kwargs: Any\n"
    "        ) -> None:\n"
    "            # DO NOT EDIT MANUALLY!!!\n"
    "            # This method was auto-generated via `butcher`\n"
    "            # Is needed only for type checking and IDE support without any additional plugins\n"
    "\n"
)

LINE_LENGTH_LIMIT = 128
MIN_VARIANTS = 2  # a variant list needs at least two members  # ruff line-length for this project

SCALARS = {
    "Integer": "int",
    "String": "str",
    "Boolean": "bool",
    "Float": "float",
    "True": "bool",
}

# Custom/union modules that do not follow the snake_case(class) convention.
MODULE_OVERRIDES = {
    "DateTime": "custom",
    "InputFile": "input_file",
}

NON_REF_NAMES = frozenset({"None", "True", "False", "Literal", "Optional", "Union", "Annotated", "Any"})

# Schema fields with date semantics that map to the DateTime custom type.
DATETIME_FIELDS = frozenset({"date", "edit_date", "forward_date", "start_date", "expiration_date", "exchange_date"})


def config_key(name: str) -> str:
    """API object name -> class-name config key (sendPhoto -> SendPhoto)."""
    return name[:1].upper() + name[1:]


def _method_class_name(name: str) -> str:
    """Alias of :func:`config_key` for method classes."""
    return config_key(name)


def class_name(name: str) -> str:
    """snake_case module -> CamelCase class name."""
    return "".join(part.capitalize() for part in name.split("_"))


def module_for(name: str) -> str:
    """Import module name for a type reference."""
    return MODULE_OVERRIDES.get(name, snake_case(name))


def load_yaml(name: str) -> dict[str, Any]:
    path = CONFIG_DIR / name
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def render_docstring(obj: ObjectSpec) -> str:
    """Class docstring: description + source link, indented for a class body."""
    text = obj.rst_description.strip() + f"\n\nSource: https://core.telegram.org/bots/api#{obj.anchor}"
    indented = "\n".join(("    " + line if line else line) for line in text.split("\n"))
    return f'    """\n{indented}\n    """'


def render_field_docstring(fld: FieldSpec | None, deprecated: dict[str, Any] | None) -> str:
    text = fld.rst_description.strip() if fld is not None else (deprecated or {}).get("docstring", "").strip()
    if deprecated:
        version = deprecated.get("version", "")
        url = deprecated.get("url", "")
        text += f"\n\n.. deprecated:: API:{version}\n   {url}"
    return text


@dataclass
class FieldRender:
    """A fully resolved field ready for rendering."""

    name: str
    annotation: str
    default_expr: str | None = None
    docstring: str = ""
    deprecated: dict[str, Any] | None = dc_field(default=None)
    alias: str | None = None

    def field_lines(self) -> str:
        default = self.default_expr
        if self.alias is not None:
            if default is None:
                default = f'Field(..., alias="{self.alias}")'
            elif default == "None":
                default = f'Field(None, alias="{self.alias}")'
            elif default.startswith("Field("):
                default = default[:-1] + f', alias="{self.alias}")'
        if default is None:
            return f"    {self.name}: {self.annotation}\n" f'''    """{self.docstring}"""'''
        line = f"    {self.name}: {self.annotation} = {default}"
        return f"{line}\n" f'''    """{self.docstring}"""'''

    def init_lines(self) -> str:
        if self.default_expr is None:
            return f"            {self.name}: {self.annotation},"
        default = self.default_expr
        if default.startswith("Field("):
            # Deprecated field markers are not repeated in the typed __init__.
            default = "None"
        return f"            {self.name}: {self.annotation} = {default},"


def render_auto_init(fields: list[FieldRender]) -> str:
    """Render the auto-generated TYPE_CHECKING ``__init__`` block.

    Required parameters are moved ahead of optional ones (python syntax
    demands it when the curated field order interleaves them). Layout
    matches the legacy generator: short signatures stay on one line, long
    ones explode with magic trailing commas so ruff format preserves them.
    """
    ordered = [f for f in fields if f.default_expr is None] + [f for f in fields if f.default_expr is not None]
    params = [f.init_lines() for f in ordered]
    args = [f"                {f.name}={f.name}," for f in ordered]
    single_def = (
        "        def __init__(__pydantic__self__, *, "
        + ", ".join(line.strip().rstrip(",") for line in params)
        + ", **__pydantic_kwargs: Any) -> None:"
    )
    if len(single_def) <= LINE_LENGTH_LIMIT:
        def_line = single_def
    else:
        def_line = (
            "        def __init__(\n"
            "            __pydantic__self__,\n"
            "            *,\n" + "\n".join(params) + "\n" + "            **__pydantic_kwargs: Any,\n" + "        ) -> None:"
        )
    single_call = "            super().__init__(" + ", ".join(f"{f.name}={f.name}" for f in fields) + ", **__pydantic_kwargs)"
    if len(single_call) <= LINE_LENGTH_LIMIT:
        call_block = single_call
    else:
        call_block = (
            "            super().__init__(\n"
            + "\n".join(args)
            + "\n"
            + "                **__pydantic_kwargs,\n"
            + "            )"
        )
    return (
        "    if TYPE_CHECKING:\n"
        "        # DO NOT EDIT MANUALLY!!!\n"
        "        # This section was auto-generated via `butcher`\n"
        "\n" + def_line + "\n" + "            # DO NOT EDIT MANUALLY!!!\n"
        "            # This method was auto-generated via `butcher`\n"
        "            # Is needed only for type checking and IDE support without any additional plugins\n"
        "\n" + call_block + "\n"
    )


class TypeResolver:
    """Resolves schema field types into python annotations."""

    def __init__(self, schema: Schema, registry: EnumRegistry) -> None:
        self.schema = schema
        self.registry = registry
        self.type_overrides: dict[str, dict[str, str]] = load_yaml("type_overrides.yml")
        self.defaults: dict[str, dict[str, str]] = load_yaml("defaults.yml")
        self.deprecations: dict[str, dict[str, Any]] = load_yaml("deprecations.yml")
        renames_cfg = load_yaml("renames.yml")
        self.renames: dict[str, str] = dict(renames_cfg.get("renames", {}))
        self.curated_defaults: dict[str, dict[str, str]] = load_yaml("curated_defaults.yml")
        self._curated_default_hints: dict[str, dict[str, bool]] = defaultdict(dict)
        self.union_aliases: dict[str, str] = {}
        self.union_by_members: dict[frozenset[str], str] = {}
        for path in (REPO_ROOT / "litegram" / "types").glob("*_union.py"):
            alias = class_name(path.stem)
            self.union_aliases[alias.removesuffix("Union")] = alias
            m = re.search(r"type \w+ = (.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
            if m:
                members = frozenset(m.group(1).split(" | "))
                self.union_by_members[members] = alias

    def union_alias(self, base: str) -> str | None:
        return self.union_aliases.get(base)

    def rule_annotation(self, fld: FieldSpec) -> str:
        """Rule-based annotation derived from a schema type string."""
        t = fld.type.strip()
        if t.startswith("Array of Array of "):
            inner = t.removeprefix("Array of Array of ")
            return f"list[list[{self._scalar_or_ref(inner)}]]"
        if t.startswith("Array of "):
            inner = t.removeprefix("Array of ")
            alias = self._variant_list_alias(inner)
            if alias is not None:
                return f"list[{alias}]"
            return f"list[{self._scalar_or_ref(inner)}]"
        if t == "Integer or String":
            return "ChatIdUnion"
        if t == "InputFile or String":
            return "InputFileUnion"
        if t in SCALARS:
            base_type = SCALARS[t]
            if base_type == "int" and fld.name in DATETIME_FIELDS:
                return "DateTime"
            return base_type
        if t == "InputFile":
            return "InputFile"
        alias = self._variant_list_alias(t) or self.union_alias(t)
        if alias is not None:
            return alias
        return t

    def _variant_list_alias(self, t: str) -> str | None:
        """Resolve ``A, B or C`` style variant lists to a union alias."""
        if " or " not in t and "," not in t:
            return None
        parts = re.split(r" or |, | and ", t)
        parts = [p.strip() for p in parts if p.strip()]
        if len(parts) < MIN_VARIANTS or any(p in SCALARS or p == "InputFile" for p in parts):
            return None
        return self.union_by_members.get(frozenset(parts))

    def _scalar_or_ref(self, t: str) -> str:
        if t in SCALARS:
            return SCALARS[t]
        if t == "Integer or String":
            return "ChatIdUnion"
        if t == "InputFile or String":
            return "InputFileUnion"
        alias = self.union_alias(t)
        if alias is not None:
            return alias
        return t

    def resolve_annotation(self, obj: ObjectSpec, fld: FieldSpec, old: FieldSpec | None) -> str:
        """Resolve an annotation for a field.

        Fields that existed in the previous schema keep their curated
        override unless it is rule-consistent with the old type (in which
        case the rules decide for the new type); brand-new fields are
        rule-derived.
        """
        override = self.type_overrides.get(config_key(obj.name), {}).get(fld.name)
        rule_new = self.rule_annotation(fld)
        if old is None:
            return rule_new
        rule_old = self.rule_annotation(old)
        if override is not None and override == rule_old:
            return rule_new
        if override is not None:
            # Curated annotation: reuse its default value too, if recorded.
            self._curated_default_hints[config_key(obj.name)][fld.name] = True
            return override
        return rule_new

    def default_expr(self, obj: ObjectSpec, fld: FieldSpec) -> str | None:
        key = config_key(obj.name)
        if self._curated_default_hints.get(key, {}).get(fld.name):
            # Curated annotation kept verbatim: keep its recorded default.
            return self.curated_defaults.get(key, {}).get(fld.name)
        if fld.required:
            return None
        default_name = self.defaults.get(key, {}).get(fld.name)
        if default_name:
            return f'Default("{default_name}")'
        if fld.name in self.deprecations.get(key, {}):
            return 'Field(None, json_schema_extra={"deprecated": True})'
        return "None"

    def render_field(self, obj: ObjectSpec, fld: FieldSpec, old: FieldSpec | None) -> FieldRender:
        rename = self.renames.get(fld.name)
        annotation = self.resolve_annotation(obj, fld, old)
        default_expr = self.default_expr(obj, fld)
        if not fld.required and annotation != "InputFile":
            if default_expr and default_expr.startswith("Default("):
                if "Default" not in annotation:
                    annotation += " | Default | None"
            elif not annotation.endswith(" | None"):
                annotation += " | None"
        return FieldRender(
            name=rename or fld.name,
            alias=fld.name if rename else None,
            annotation=annotation,
            default_expr=default_expr,
            docstring=render_field_docstring(fld, self.deprecations.get(config_key(obj.name), {}).get(fld.name)),
            deprecated=self.deprecations.get(config_key(obj.name), {}).get(fld.name),
        )


class Generator:
    """Top-level code generation entry point."""

    def __init__(self, schema: Schema, old_schema: Schema | None = None) -> None:
        self.schema = schema
        self.old_schema = old_schema
        self.registry = EnumRegistry.load()
        self.resolver = TypeResolver(schema, self.registry)
        bases = load_yaml("bases.yml")
        self.mutable_types: set[str] = set(bases.get("mutable", []))
        self.special_bases: dict[str, str] = dict(bases.get("special", {}))
        self.field_order: dict[str, list[str]] = load_yaml("field_order.yml")

    def ordered_fields(self, obj: ObjectSpec) -> list[FieldSpec]:
        """Fields in code order when curated, otherwise page order."""
        order = self.field_order.get(config_key(obj.name))
        if order is None:
            return obj.annotations
        by_name = {f.name: f for f in obj.annotations}
        ordered = [by_name[n] for n in order if n in by_name]
        # New fields (not yet in the curated order) follow in page order.
        ordered.extend(f for f in obj.annotations if f not in ordered)
        return ordered

    def base_class_for(self, obj: ObjectSpec) -> str:
        """Base class of the generated type class."""
        special = self.special_bases.get(config_key(obj.name))
        if special is not None:
            return special
        if config_key(obj.name) in self.mutable_types:
            return "MutableTelegramObject"
        family = self.registry.family_of(obj.name)
        if family is not None and family.base:
            return family.base
        return "TelegramObject"

    # --- lookups -------------------------------------------------------------

    def _old_field(self, obj: ObjectSpec, fld: FieldSpec) -> FieldSpec | None:
        if self.old_schema is None:
            return None
        old_obj = self.old_schema.object(obj.name)
        if old_obj is None:
            return None
        return old_obj.field(fld.name)

    def _deprecated_extras(self, obj: ObjectSpec) -> list[FieldRender]:
        """Deprecated fields kept in code but absent from the docs page."""
        deps = self.resolver.deprecations.get(config_key(obj.name), {})
        known = {f.name for f in obj.annotations}
        extras: list[FieldRender] = []
        for name, dep in deps.items():
            if name in known or not dep.get("annotation"):
                continue
            extras.append(
                FieldRender(
                    name=name,
                    annotation=dep["annotation"],
                    default_expr='Field(None, json_schema_extra={"deprecated": True})',
                    docstring=render_field_docstring(None, dep),  # type: ignore[arg-type]
                    deprecated=dep,
                )
            )
        return extras

    def _variant_value(self, obj: ObjectSpec, family: Family) -> str | None:
        fld = obj.field(family.attribute)
        if fld is None:
            return None
        return extract_family_value(fld.rst_description, family.regexp)

    def _deprecated_extra_fields(self, obj: ObjectSpec) -> list[FieldSpec]:
        """Deprecated fields kept in code although absent from the page."""
        deps = self.resolver.deprecations.get(config_key(obj.name), {})
        return [
            FieldSpec(
                name=name,
                type="Boolean" if deps[name].get("version") else "",
                required=False,
                description="",
                html_description="",
                rst_description="",
            )
            for name in deps
            if obj.field(name) is None
        ]

    # --- type files ------------------------------------------------------------

    def render_type_file(self, obj: ObjectSpec) -> str:
        family = self.registry.family_of(obj.name)
        if family is not None:
            return self._render_variant_type_file(obj, family)
        return self._render_plain_type_file(obj)

    def _render_plain_type_file(self, obj: ObjectSpec) -> str:
        fields = [self.resolver.render_field(obj, f, self._old_field(obj, f)) for f in self.ordered_fields(obj)]
        fields.extend(self._deprecated_extras(obj))
        tc_refs = self._type_checking_refs(obj.name, fields)
        header = self._type_file_imports(obj, tc_refs, fields)
        field_block = "\n".join(f.field_lines() for f in fields)
        init_block = render_auto_init(fields) if fields else ""
        return (
            header
            + f"\n\nclass {obj.name}({self.base_class_for(obj)}):\n"
            + render_docstring(obj)
            + "\n"
            + field_block
            + ("\n\n" + init_block if init_block else "")
        )

    def _render_variant_type_file(self, obj: ObjectSpec, family: Family) -> str:
        fields = [self.resolver.render_field(obj, f, self._old_field(obj, f)) for f in self.ordered_fields(obj)]
        fields.extend(self._deprecated_extras(obj))
        value = self._variant_value(obj, family)
        member = value.upper() if value else None
        for f in fields:
            if f.name == family.attribute and member:
                f.annotation = f"Literal[{family.enum_name}.{member}]"
                f.default_expr = f"{family.enum_name}.{member}"
        tc_refs = self._type_checking_refs(obj.name, fields)
        header = self._variant_file_imports(obj, family, tc_refs)
        field_block = "\n".join(f.field_lines() for f in fields)
        init_block = render_auto_init(fields) if fields else ""
        base_class = self.base_class_for(obj)
        return (
            header
            + f"\n\nclass {obj.name}({base_class}):\n"
            + render_docstring(obj)
            + "\n"
            + field_block
            + ("\n\n" + init_block if init_block else "")
        )

    # --- method files ------------------------------------------------------------

    def render_method_file(self, obj: ObjectSpec) -> str:
        fields = [self.resolver.render_field(obj, f, self._old_field(obj, f)) for f in self.ordered_fields(obj)]
        fields.extend(self._deprecated_extras(obj))
        returning = self._returning_type(obj)
        header = self._method_file_imports(obj, returning, fields)
        field_block = "\n".join(f.field_lines() for f in fields)
        init_block = render_auto_init(fields) if fields else ""
        return (
            header
            + f"\n\nclass {_method_class_name(obj.name)}(TelegramMethod[{returning}]):\n"
            + render_docstring(obj)
            + "\n"
            + "\n"
            + f"    __returning__ = {returning}\n"
            + f'    __api_method__ = "{obj.name}"\n'
            + "\n"
            + field_block
            + ("\n\n" + init_block if init_block else "")
        )

    def _returning_type(self, obj: ObjectSpec) -> str:
        """Return type derived from the method description."""
        desc = obj.rst_description
        m = re.search(
            r"(?:the sent |an? ):class:`litegram\.types\.[a-z_0-9]+\.([A-Za-z0-9]+)`(?: object)? is returned",
            desc,
        )
        if m:
            return m.group(1)
        m = re.search(
            r"[Rr]eturns an [Aa]rray of (?:the sent |new )?:class:`litegram\.types\.[a-z_0-9]+\.([A-Za-z0-9]+)`",
            desc,
        )
        if m:
            return f"list[{m.group(1)}]"
        m = re.search(
            r"[Rr]eturns a :class:`litegram\.types\.[a-z_0-9]+\.([A-Za-z0-9]+)`",
            desc,
        )
        if m:
            return m.group(1)
        m = re.search(
            r"[Aa]rray of :class:`litegram\.types\.[a-z_0-9]+\.([A-Za-z0-9]+)` objects",
            desc,
        )
        if m:
            return f"list[{m.group(1)}]"
        if re.search(r"[Rr]eturns .* as \*String\*", desc):
            return "str"
        if re.search(r"[Rr]eturns .* as \*Integer\*", desc):
            return "int"
        return "bool"

    # --- unions and enums -----------------------------------------------------------

    def render_union_file(self, family: Family) -> str:
        members = family.variants
        imports = "\n".join(f"from .{snake_case(m)} import {m}" for m in sorted(members))
        alias = self.resolver.union_alias(family.base or "")
        expr = " | ".join(members)
        return f"from __future__ import annotations\n\nfrom typing import TypeAlias\n\n{imports}\n\ntype {alias} = {expr}\n"

    def render_enum_file(self, family: Family, values: dict[str, str]) -> str:
        body = "\n".join(f'    {value.upper()} = "{value}"' for value in values.values())
        desc_lines = (family.description or "").strip().split("\n")
        desc = "\n    ".join(desc_lines)
        return (
            "from __future__ import annotations\n\n"
            "from enum import Enum\n\n\n"
            f"class {family.enum_name}(str, Enum):\n"
            f'    """\n'
            f"    {desc}\n"
            f'    """\n\n'
            f"{body}\n"
        )

    # --- shared helpers ---------------------------------------------------------------

    def _type_checking_refs(self, self_name: str, fields: list[FieldRender]) -> list[str]:
        """Names referenced by fields that need TYPE_CHECKING imports.

        Excludes enum member names (all caps), python keywords, the family
        enum and the imported base classes.
        """
        refs: set[str] = set()
        family = self.registry.family_of(self_name)
        base = self.base_class_for(self._fake_object(self_name))
        excluded = {self_name, "TelegramObject", "MutableTelegramObject", base, "Default"}
        if family is not None:
            excluded.add(family.enum_name)
            excluded.add(family.base or "")
        for f in fields:
            for ident in re.findall(r"\b([A-Z][A-Za-z0-9]*)\b", f.annotation):
                if ident in excluded or ident.isupper() or ident in NON_REF_NAMES:
                    continue
                refs.add(ident)
        return sorted(refs)

    def _fake_object(self, name: str) -> ObjectSpec:
        obj = self.schema.object(name)
        if obj is None:
            obj = ObjectSpec(
                anchor=name.lower(),
                name=name,
                description="",
                html_description="",
                rst_description="",
                category="types",
            )
        return obj

    def _type_file_imports(self, obj: ObjectSpec, refs: list[str], fields: list[FieldRender] | None = None) -> str:
        base = self.base_class_for(obj)
        lines = ["from __future__ import annotations", ""]
        # TYPE_CHECKING is always imported: the auto-generated __init__ uses it.
        lines.extend(("from typing import TYPE_CHECKING, Any", ""))
        if fields and any((f.default_expr and "Field(" in f.default_expr) or f.alias is not None for f in fields):
            lines.extend(("from pydantic import Field", ""))
        if base in {"TelegramObject", "MutableTelegramObject"}:
            lines.append(f"from .base import {base}")
        elif base not in {obj.name, "ABC", "Protocol"}:
            # A real parent object (e.g. ChatFullInfo -> Chat).
            lines.extend((f"from .{snake_case(base)} import {base}", ""))
        if refs:
            lines.append("if TYPE_CHECKING:")
            lines.extend(f"    from .{module_for(ref)} import {ref}" for ref in refs)
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def _variant_file_imports(self, obj: ObjectSpec, family: Family, refs: list[str]) -> str:
        base = family.base or ""
        lines = ["from __future__ import annotations", ""]
        lines.extend(("from typing import TYPE_CHECKING, Any, Literal", ""))
        lines.append(f"from ..enums import {family.enum_name}")
        if base:
            lines.append(f"from .{module_for(base)} import {base}")
        lines.append("")
        if refs:
            lines.append("if TYPE_CHECKING:")
            lines.extend(f"    from .{module_for(ref)} import {ref}" for ref in refs)
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def _method_file_imports(self, obj: ObjectSpec, returning: str, fields: list[FieldRender]) -> str:
        """Methods import every referenced name directly from ``..types``."""
        names: set[str] = {
            self.resolver.union_alias(ident) or ident
            for f in fields
            for ident in re.findall(r"\b([A-Z][A-Za-z0-9]*)\b", f.annotation)
            if not ident.isupper() and ident not in NON_REF_NAMES
        }
        for ident in re.findall(r"\b([A-Z][A-Za-z0-9]*)\b", returning):
            if ident in {"TelegramMethod", "list", "bool"}:
                continue
            names.add(self.resolver.union_alias(ident) or ident)
        names.discard("Default")
        uses_default = any(f.default_expr and "Default(" in f.default_expr for f in fields)
        uses_field = any((f.default_expr and "Field(" in f.default_expr) or f.alias is not None for f in fields)
        lines = ["from __future__ import annotations", ""]
        lines.extend(("from typing import TYPE_CHECKING, Any", ""))
        if uses_field:
            lines.extend(("from pydantic import Field", ""))
        if uses_default:
            lines.append("from ..client.default import Default")
        if names:
            lines.append("from ..types import (")
            lines.extend(f"    {name}," for name in sorted(names))
            lines.append(")")
        lines.extend(("from .base import TelegramMethod", ""))
        return "\n".join(lines).rstrip() + "\n"
