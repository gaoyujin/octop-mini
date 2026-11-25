from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mini.api.app import build_app
from mini.infra.boot import boot_control_plane
from mini.infra.config import load_config
from mini.infra.paths import PathLayout
from mini.infra.runtime import MiniRuntime


def _client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    layout = PathLayout.from_env()
    cfg = load_config(layout=layout)
    runtime = MiniRuntime(layout=layout, config=cfg)
    boot_control_plane(runtime)
    runtime.services.user_manager.create_user("alice", "secret123")
    return TestClient(build_app(runtime))


def test_settings_bind_requires_jwt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        unauth = client.get("/api/settings/bind")
        assert unauth.status_code == 401
        assert unauth.json()["code"] == "MISSING_BEARER_TOKEN"

        login = client.post("/api/auth/login", json={"username": "alice", "password": "secret123"})
        token = login.json()["access_token"]
        ok = client.get("/api/settings/bind", headers={"Authorization": f"Bearer {token}"})
        assert ok.status_code == 200
        body = ok.json()
        assert body["bind_host"] == "127.0.0.1"
        assert body["port"] == 8765