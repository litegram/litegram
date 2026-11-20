"""Schema access helpers shared by the diff and code generation stages."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from dataclasses import field as dc_field
from functools import cached_property
from pathlib import Path  # noqa: TC003 — used at runtime (load)
from typing import Any


def snake_case(name: str) -> str:
    """Convert CamelCase/lowerCamelCase API name to snake_case module name."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


@dataclass
class FieldSpec:
    """One annotation (field or method parameter) of an API object."""

    name: str
    type: str
    required: bool
    description: str
    html_description: str
    rst_description: str

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> FieldSpec:
        return cls(
            name=raw["name"],
            type=raw["type"],
            required=raw["required"],
            description=raw["description"],
            html_description=raw["html_description"],
            rst_description=raw["rst_description"],
        )


@dataclass
class ObjectSpec:
    """One API object (type or method) parsed from the docs page."""

    anchor: str
    name: str
    description: str
    html_description: str
    rst_description: str
    category: str  # "types" | "methods"
    annotations: list[FieldSpec] = dc_field(default_factory=list)

    @classmethod
    def from_json(cls, raw: dict[str, Any]) -> ObjectSpec:
        return cls(
            anchor=raw["anchor"],
            name=raw["name"],
            description=raw["description"],
            html_description=raw["html_description"],
            rst_description=raw["rst_description"],
            category=raw["category"],
            annotations=[FieldSpec.from_json(a) for a in raw.get("annotations", [])],
        )

    @property
    def module_name(self) -> str:
        return snake_case(self.name)

    @property
    def is_method(self) -> str:
        return self.category == "methods"

    def field(self, name: str) -> FieldSpec | None:
        return next((a for a in self.annotations if a.name == name), None)


class Schema:
    """Loaded Bot API schema with convenient lookups."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.version: str = data["api"]["version"]
        self.release_date: str = data["api"]["release_date"]
        self.groups: list[dict[str, Any]] = data["items"]
        self._objects: dict[str, ObjectSpec] = {}
        self._anchors: dict[str, str] = {}
        for group in self.groups:
            for raw in group["children"]:
                spec = ObjectSpec.from_json(raw)
                self._objects[spec.name] = spec
                self._anchors[spec.anchor.lower()] = spec.name

    @classmethod
    def load(cls, path: Path) -> Schema:
        return cls(json.loads(path.read_text(encoding="utf-8")))

    @cached_property
    def types(self) -> list[ObjectSpec]:
        return [o for o in self._objects.values() if o.category == "types"]

    @cached_property
    def methods(self) -> list[ObjectSpec]:
        return [o for o in self._objects.values() if o.category == "methods"]

    def object(self, name: str) -> ObjectSpec | None:
        return self._objects.get(name)

    def all_objects(self) -> list[ObjectSpec]:
        return list(self._objects.values())

    def by_anchor(self, anchor: str) -> ObjectSpec | None:
        return self.object(self._anchors.get(anchor.lower(), ""))

    def all_names(self) -> list[str]:
        return list(self._objects)
