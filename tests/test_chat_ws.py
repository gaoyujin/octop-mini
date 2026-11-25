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
    return TestClient(build_app(runtime))


def test_ws_requires_running_agent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        login = client.post("/api/auth/login", json={"username": "alice", "password": "secret123"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        agent_id = client.post("/api/agents", json={"name": "bot"}, headers=headers).json()["agent_id"]
        thread_id = client.post(
            f"/api/agents/{agent_id}/threads", json={}, headers=headers
        ).json()["thread_id"]

        with client.websocket_connect(f"/api/agents/{agent_id}/chat/ws?token={token}") as ws:
            ws.send_json({"type": "user_turn", "thread_id": thread_id, "text": "hi"})
            err = ws.receive_json()
            assert err["type"] == "error"
            assert err["code"] == "AGENT_NOT_RUNNING"

        client.post(f"/api/agents/{agent_id}/start", headers=headers)
        with client.websocket_connect(f"/api/agents/{agent_id}/chat/ws?token={token}") as ws:
            ws.send_json({"type": "user_turn", "thread_id": thread_id, "text": "hi"})
            assert ws.receive_json()["type"] == "assistant_text"
            assert ws.receive_json()["type"] == "done"