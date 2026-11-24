"""Filesystem layout under ``MINI_HOME`` (teaching counterpart to Octop ``PathLayout``)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PathLayout:
    """All user-data paths derive from ``root`` — no hard-coded drive letters in callers."""

    root: Path

    @classmethod
    def from_env(cls) -> PathLayout:
        """Resolve install root from ``MINI_HOME`` or ``~/.octop-mini``."""
        raw = os.environ.get("MINI_HOME", "").strip()
        if raw:
            return cls(Path(raw).expanduser().resolve())
        return cls((Path.home() / ".octop-mini").resolve())

    @property
    def config(self) -> Path:
        return self.root / "config.json"

    @property
    def db(self) -> Path:
        return self.root / "mini.db"

    @property
    def agents_dir(self) -> Path:
        return self.root / "agents"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"

    @property
    def log_file(self) -> Path:
        return self.logs_dir / "mini.log"

    def ensure_root(self) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        return self.root

    def ensure_logs_dir(self) -> Path:
        out = self.logs_dir
        out.mkdir(parents=True, exist_ok=True)
        return out

    def agent_workspace(self, agent_id: str) -> Path:
        return self.agents_dir / agent_id


def resolve_mini_home() -> Path:
    """Compat helper: ``PathLayout.from_env().root``."""
    return PathLayout.from_env().root


def config_file_path() -> Path:
    """Compat helper: ``PathLayout.from_env().config``."""
    return PathLayout.from_env().config