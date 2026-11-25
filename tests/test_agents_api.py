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
    services = boot_control_plane(runtime)
    services.user_manager.create_user("alice", "secret123")
    services.user_manager.create_user("bob", "secret456")
    return TestClient(build_app(runtime))


def _token(client: TestClient, username: str, password: str) -> str:
    login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login.status_code == 200
    return str(login.json()["access_token"])


def test_create_start_stop_and_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with _client(tmp_path, monkeypatch) as client:
        token = _token(client, "alice", "secret123")
        headers = {"Authorization": f"Bearer {token}"}

        created = client.post("/api/agents", json={"name": "lab-bot"}, headers=headers)
        assert created.status_code == 200
        body = created.json()
        agent_id = body["agent_id"]
        assert body["last_state"] == "stopped"
        assert agent_id.startswith("ag_")

        workspace = PathLayout.from_env().agent_workspace(agent_id)
        assert (workspace / "SOUL.md").is_file()

        started = client.post(f"/api/agents/{agent_id}/start", headers=headers)
        assert started.status_code == 200
        assert started.json()["state"] == "running"

        again = client.post(f"/api/agents/{agent_id}/start", headers=headers)
        assert again.status_code == 409
        assert again.json()["code"] == "AGENT_ALREADY_RUNNING"

        stopped = client.post(f"/api/agents/{agent_id}/stop", headers=headers)
        assert stopped.status_code == 200
        assert stopped.json()["state"] == "stopped"

        listed = client.get("/api/agents", headers=headers)
        assert listed.status_code == 200
        assert len(listed.json()["agents"]) == 1


def test_other_user_cannot_start_agent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        alice_headers = {"Authorization": f"Bearer {_token(client, 'alice', 'secret123')}"}
        created = client.post("/api/agents", json={"name": "private"}, headers=alice_headers)
        agent_id = created.json()["agent_id"]

        bob_headers = {"Authorization": f"Bearer {_token(client, 'bob', 'secret456')}"}
        denied = client.post(f"/api/agents/{agent_id}/start", headers=bob_headers)
        assert denied.status_code == 403
        assert denied.json()["code"] == "FORBIDDEN"