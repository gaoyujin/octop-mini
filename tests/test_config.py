from __future__ import annotations

import json
from pathlib import Path

import pytest

from mini.infra.config import MiniConfig, env_bind_overrides, load_config


def test_load_config_creates_defaults(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MINI_PORT", raising=False)
    monkeypatch.delenv("MINI_BIND_HOST", raising=False)
    cfg_path = tmp_path / "config.json"
    cfg = load_config(cfg_path)
    assert cfg == MiniConfig()
    assert cfg_path.exists()
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    assert data["port"] == 8765


def test_load_config_reads_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MINI_PORT", raising=False)
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(
        json.dumps({"bind_host": "0.0.0.0", "port": 18080}),
        encoding="utf-8",
    )
    cfg = load_config(cfg_path)
    assert cfg.bind_host == "0.0.0.0"
    assert cfg.port == 18080


def test_env_overrides_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"port": 18080}), encoding="utf-8")
    monkeypatch.setenv("MINI_PORT", "19090")
    cfg = load_config(cfg_path)
    assert cfg.port == 19090


def test_env_bind_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MINI_BIND_HOST", raising=False)
    monkeypatch.delenv("MINI_PORT", raising=False)
    assert env_bind_overrides() == (None, None)