"""Enum/family registry for discriminated object families.

Every ``multi_parse`` enum config defines a family: a base API object whose
variants are separate classes with a literal-typed discriminator field, an
``XxxUnion`` alias and a ``str`` enum. The registry maps family bases to
their variant classes and enum values.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parent / "config" / "enums"
LEGACY_CONFIG_DIR = Path(__file__).resolve().parents[2] / ".butcher" / "enums"


VALUE_PATTERNS = (
    r"always '([a-z_0-9]+)'",
    r"must be \*([a-z_0-9]+)\*",
    r"always \*([a-z_0-9]+)\*",
    r":code:`([a-z_0-9]+)`",
    r"'([a-z_0-9]+)'",
    r"must be ([a-z_0-9]+)",
    r"\b([a-z_0-9]+)\b",
)


def extract_family_value(text: str, regexp: str | None) -> str | None:
    """Extract the discriminator value from a variant field description.

    Tries the configured regexp first (mirrors the legacy butcher configs),
    then a cascade of description phrasings used across API versions.
    """
    if regexp:
        m = re.search(regexp, text)
        if m and m.group(1):
            return m.group(1)
    for pattern in VALUE_PATTERNS[:-1]:
        m = re.search(pattern, text)
        if m:
            return m.group(1)
    return None


@dataclass
class Family:
    """A discriminated object family (e.g. MessageOrigin -> MessageOriginUser...)."""

    enum_name: str
    base: str | None
    variants: list[str]
    attribute: str
    regexp: str | None
    description: str | None = None
    static: dict[str, str] | None = None
    extract_exclude: list[str] | None = None

    @property
    def has_variants(self) -> bool:
        return bool(self.variants)


class EnumRegistry:
    """Loads enum configs and exposes family lookups."""

    def __init__(self, configs: dict[str, dict]) -> None:
        self._configs = configs

    @classmethod
    def load(cls) -> EnumRegistry:
        configs: dict[str, dict] = {}
        for source in (LEGACY_CONFIG_DIR, CONFIG_DIR):
            if not source.is_dir():
                continue
            for path in sorted(source.glob("*.yml")):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                data["_source"] = path
                configs[data["name"]] = data
        return cls(configs)

    @cached_property
    def families(self) -> dict[str, Family]:
        """All multi_parse families keyed by the base object name."""
        result: dict[str, Family] = {}
        for name, cfg in self._configs.items():
            mp = cfg.get("multi_parse")
            if not mp:
                continue
            entities = mp.get("entities", [])
            base = _derive_base(entities)
            result[base] = Family(
                enum_name=name,
                base=base,
                variants=entities,
                attribute=mp.get("attribute", "type"),
                regexp=mp.get("regexp"),
                description=cfg.get("description"),
                static=mp.get("static"),
            )
        return result

    @cached_property
    def simple_enums(self) -> dict[str, Family]:
        """Non-variant enums (parse/extract/static modes) by enum name."""
        result: dict[str, Family] = {}
        for name, cfg in self._configs.items():
            if "multi_parse" in cfg:
                continue
            mode = "extract" if "extract" in cfg else "parse" if "parse" in cfg else "static"
            spec = cfg.get(mode, {}) if mode != "static" else {}
            result[name] = Family(
                enum_name=name,
                base=spec.get("entity"),
                variants=[],
                attribute=spec.get("attribute", ""),
                regexp=spec.get("regexp"),
                description=cfg.get("description"),
                static=cfg.get("static"),
                extract_exclude=(spec.get("exclude") if mode == "extract" else None),
            )
        return result

    def family_of(self, object_name: str) -> Family | None:
        """Family for which the given object is a variant."""
        for family in self.families.values():
            if object_name in family.variants:
                return family
        return None

    def family_for_base(self, base: str) -> Family | None:
        return self.families.get(base)


def _derive_base(variant_names: list[str]) -> str | None:
    """Derive the family base name from variant names.

    The base is the longest common prefix of all variant names, cut back to
    a camel-case word boundary when the prefix ends mid-word:

    - ``MessageOriginUser``/``MessageOriginChat``     -> ``MessageOrigin``
    - ``WidgetQueryTypeData``/``WidgetQueryTypeSignData`` -> ``WidgetQueryType``
    - ``InputMediaPhoto``/``InputMediaVideo``         -> ``InputMedia``
    """
    if not variant_names:
        return None
    prefix = variant_names[0]
    for name in variant_names[1:]:
        while prefix and not name.startswith(prefix):
            prefix = prefix[:-1]
        if not prefix:
            return None
    # Trim an incomplete trailing word: "MessageOriginU" -> "MessageOrigin".
    # A trailing single capital letter means the common prefix cut a word
    # in half; complete trailing words ("WidgetQueryType" -> "Type") stay.
    if re.search(r"[A-Z]$", prefix) and len(prefix) > 1:
        prefix = prefix[:-1]
    return prefix or None


def derive_base(variant_names: list[str]) -> str | None:
    """Public wrapper kept for tests."""
    return _derive_base(variant_names)
