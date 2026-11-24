from __future__ import annotations

import json
from pathlib import Path

import pytest

from mini.cli.bind import resolve_bind, save_configfile_overrides


def test_resolve_bind_cli_wins(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "home"
    home.mkdir()
    cfg = home / "config.json"
    cfg.write_text(json.dumps({"port": 1111}), encoding="utf-8")
    monkeypatch.setenv("MINI_HOME", str(home))
    monkeypatch.setenv("MINI_PORT", "2222")
    host, port = resolve_bind(None, 3333)
    assert port == 3333


def test_resolve_bind_env_over_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "home"
    home.mkdir()
    cfg = home / "config.json"
    cfg.write_text(json.dumps({"port": 1111}), encoding="utf-8")
    monkeypatch.setenv("MINI_HOME", str(home))
    monkeypatch.setenv("MINI_PORT", "2222")
    host, port = resolve_bind(None, None)
    assert port == 2222


def test_save_configfile_overrides(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    path = save_configfile_overrides("127.0.0.1", 9999)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["bind_host"] == "127.0.0.1"
    assert data["port"] == 9999