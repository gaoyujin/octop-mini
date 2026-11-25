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
    app = build_app(runtime)
    return TestClient(app)


def test_login_and_me(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        unauth = client.get("/api/auth/me")
        assert unauth.status_code == 401
        assert unauth.json()["code"] == "MISSING_BEARER_TOKEN"

        bad = client.post("/api/auth/login", json={"username": "alice", "password": "wrong"})
        assert bad.status_code == 401
        assert bad.json() == {"code": "INVALID_CREDENTIALS", "message": "invalid credentials"}

        login = client.post("/api/auth/login", json={"username": "alice", "password": "secret123"})
        assert login.status_code == 200
        token = login.json()["access_token"]

        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["username"] == "alice"


def test_health_stays_public(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["schema_version"] == 4