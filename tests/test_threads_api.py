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
    assert services.schema_version == 5
    services.user_manager.create_user("alice", "secret123")
    services.user_manager.create_user("bob", "secret456")
    return TestClient(build_app(runtime))


def _token(client: TestClient, username: str, password: str) -> str:
    login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login.status_code == 200
    return str(login.json()["access_token"])


def test_thread_create_list_messages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        headers = {"Authorization": f"Bearer {_token(client, 'alice', 'secret123')}"}

        agent = client.post("/api/agents", json={"name": "chat-bot"}, headers=headers)
        agent_id = agent.json()["agent_id"]
        client.post(f"/api/agents/{agent_id}/start", headers=headers)

        created = client.post(f"/api/agents/{agent_id}/threads", json={"title": "demo"}, headers=headers)
        assert created.status_code == 200
        thread_id = created.json()["thread_id"]
        assert created.json()["session_key"] == f"dashboard:{agent_id}:{thread_id}"

        listed = client.get(f"/api/agents/{agent_id}/threads", headers=headers)
        assert len(listed.json()["threads"]) == 1

        with client.websocket_connect(
            f"/api/agents/{agent_id}/chat/ws?token={_token(client, 'alice', 'secret123')}"
        ) as ws:
            ws.send_json({"type": "user_turn", "thread_id": thread_id, "text": "hello"})
            assert ws.receive_json()["text"] == "echo: hello"
            assert ws.receive_json()["type"] == "done"

        history = client.get(
            f"/api/agents/{agent_id}/threads/{thread_id}/messages",
            headers=headers,
        )
        msgs = history.json()["messages"]
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user" and msgs[0]["content"] == "hello"
        assert msgs[1]["role"] == "assistant" and "echo:" in msgs[1]["content"]


def test_other_user_cannot_read_messages(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with _client(tmp_path, monkeypatch) as client:
        alice_headers = {"Authorization": f"Bearer {_token(client, 'alice', 'secret123')}"}
        agent_id = client.post("/api/agents", json={"name": "x"}, headers=alice_headers).json()[
            "agent_id"
        ]
        thread_id = client.post(
            f"/api/agents/{agent_id}/threads", json={}, headers=alice_headers
        ).json()["thread_id"]

        bob_headers = {"Authorization": f"Bearer {_token(client, 'bob', 'secret456')}"}
        denied = client.get(
            f"/api/agents/{agent_id}/threads/{thread_id}/messages",
            headers=bob_headers,
        )
        assert denied.status_code == 403
        assert denied.json()["code"] == "FORBIDDEN"