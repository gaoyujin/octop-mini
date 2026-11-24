from __future__ import annotations

from pathlib import Path

import pytest

from mini.infra.paths import PathLayout


def test_path_layout_default_under_home(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MINI_HOME", raising=False)
    layout = PathLayout.from_env()
    assert layout.root == (Path.home() / ".octop-mini").resolve()
    assert layout.config == layout.root / "config.json"


def test_ensure_root_creates_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    base = tmp_path / "nested" / "home"
    monkeypatch.setenv("MINI_HOME", str(base))
    layout = PathLayout.from_env()
    layout.ensure_root()
    assert base.is_dir()