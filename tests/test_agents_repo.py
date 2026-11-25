from __future__ import annotations

from pathlib import Path

import pytest

from mini.infra.boot import boot_control_plane
from mini.infra.config import load_config
from mini.infra.paths import PathLayout
from mini.infra.runtime import MiniRuntime


def test_agent_repo_create_and_list(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    layout = PathLayout.from_env()
    cfg = load_config(layout=layout)
    runtime = MiniRuntime(layout=layout, config=cfg)
    services = boot_control_plane(runtime)
    assert services.schema_version == 4

    user = services.user_manager.create_user("owner", "pass12345")
    row = services.agent_repo.create(
        agent_id="ag_test0001",
        user_id=user.id,
        name="helper",
    )
    assert row.last_state == "stopped"
    listed = services.agent_repo.list_by_user_id(user.id)
    assert len(listed) == 1
    assert listed[0].agent_id == "ag_test0001"


def test_agent_name_unique_per_user(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    layout = PathLayout.from_env()
    cfg = load_config(layout=layout)
    runtime = MiniRuntime(layout=layout, config=cfg)
    services = boot_control_plane(runtime)
    user = services.user_manager.create_user("owner", "pass12345")

    from mini.infra.errors import ErrorCode, MiniError

    services.agent_manager.create_agent(user_id=user.id, name="dup")
    with pytest.raises(MiniError) as exc:
        services.agent_manager.create_agent(user_id=user.id, name="dup")
    assert exc.value.code == ErrorCode.AGENT_NAME_TAKEN