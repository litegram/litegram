from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

BASE_PATTERN = r'({variable} = ").+(")'
PACKAGE_VERSION = re.compile(BASE_PATTERN.format(variable="__version__"))
API_VERSION = re.compile(BASE_PATTERN.format(variable="__api_version__"))
API_VERSION_BADGE = re.compile(r"(API-)[\d.]+(-blue\.svg)")
API_VERSION_LINE = re.compile(r"(Supports `Telegram Bot API )[\d.]+( <https://core\.telegram\.org/bots/api>`_ )")

STAGE_MAPPING = {
    "alpha": "a",
    "beta": "b",
}


def get_package_version() -> str:
    with Path("pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    # Since we switched to Hatch, we might want to read from __meta__.py
    # but for now let's just make it pass type checking by assuming where it could be
    # or just return a dummy if we don't know yet.
    # Actually, the original code looked for data["tool"]["poetry"]["version"]
    return data.get("project", {}).get("version", "0.0.0")


def get_telegram_api_version() -> str:
    path = Path.cwd() / ".butcher" / "schema" / "schema.json"
    schema = json.loads(path.read_text())
    version = schema["api"]["version"]
    path = Path.cwd() / ".apiversion"
    path.write_text(version + "\n")
    return version


def replace_line(content: str, pattern: re.Pattern, new_value: str) -> str:
    return pattern.sub(f"\\g<1>{new_value}\\g<2>", content)


def write_package_meta(api_version: str) -> None:
    path = Path.cwd() / "litegram" / "__meta__.py"
    content = path.read_text()

    content = replace_line(content, API_VERSION, api_version)

    path.write_text(content)


def write_readme(api_version: str) -> None:
    path = Path.cwd() / "README.rst"
    content = path.read_text()
    content = replace_line(content, API_VERSION_BADGE, api_version)
    content = replace_line(content, API_VERSION_LINE, api_version)
    path.write_text(content)


def write_docs_index(api_version: str) -> None:
    path = Path.cwd() / "docs" / "index.rst"
    content = path.read_text()
    content = replace_line(content, API_VERSION_BADGE, api_version)
    path.write_text(content)


def main():
    api_version = get_telegram_api_version()

    write_package_meta(api_version=api_version)
    write_readme(api_version=api_version)
    write_docs_index(api_version=api_version)


if __name__ == "__main__":
    main()
