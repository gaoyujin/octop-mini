"""Data directory layout (M1: home + config path; M2 will extend)."""

from __future__ import annotations

import os
from pathlib import Path


def resolve_mini_home() -> Path:
    """Return ``MINI_HOME`` or ``~/.octop-mini`` (mirrors ``OCTOP_HOME``)."""
    if raw := os.environ.get("MINI_HOME"):
        return Path(raw).expanduser().resolve()
    return (Path.home() / ".octop-mini").resolve()


def config_file_path() -> Path:
    """``{MINI_HOME}/config.json``."""
    return resolve_mini_home() / "config.json"