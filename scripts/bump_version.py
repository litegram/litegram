#!/usr/bin/env python3
"""Version bumping script for litegram (replaces hatch version)."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def bump_version(part: str) -> str:
    """Bump version in __meta__.py."""
    meta_path = Path("litegram/__meta__.py")
    content = meta_path.read_text()

    # Extract current version
    version_match = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not version_match:
        raise ValueError("Could not find version in __meta__.py")

    major, minor, patch = map(int, version_match.groups())

    # Bump appropriate part
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    elif part.startswith("to:"):
        new_version = part.replace("to:", "")
        content = re.sub(r'__version__ = "\d+\.\d+\.\d+"', f'__version__ = "{new_version}"', content)
        meta_path.write_text(content)
        return new_version
    else:
        raise ValueError(f"Unknown part: {part}. Use major, minor, patch, or to:X.Y.Z")

    new_version = f"{major}.{minor}.{patch}"
    content = re.sub(r'__version__ = "\d+\.\d+\.\d+"', f'__version__ = "{new_version}"', content)
    meta_path.write_text(content)
    return new_version


if __name__ == "__main__":
    REQUIRED_ARGS_COUNT = 2
    if len(sys.argv) != REQUIRED_ARGS_COUNT:
        sys.exit(1)

    new_version = bump_version(sys.argv[1])
