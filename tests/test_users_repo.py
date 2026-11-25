from __future__ import annotations

from pathlib import Path

import pytest

from mini.infra.boot import boot_control_plane
from mini.infra.config import load_config
from mini.infra.db.factory import open_database
from mini.infra.db.migrate import current_schema_version, run_migrations
from mini.infra.paths import PathLayout
from mini.infra.runtime import MiniRuntime


def test_user_repo_create_and_get(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    layout = PathLayout.from_env()
    layout.ensure_root()
    pool = open_database(layout)
    run_migrations(pool)
    assert current_schema_version(pool) == 4

    cfg = load_config(layout=layout)
    runtime = MiniRuntime(layout=layout, config=cfg)
    services = boot_control_plane(runtime)
    repo = services.user_repo

    manager = services.user_manager
    assert repo.get_by_username("alice") is None
    created = manager.create_user("alice", "pass")
    assert created.username == "alice"
    assert created.id > 0
    assert created.password_hash is not None

    loaded = repo.get_by_username("alice")
    assert loaded is not None
    assert loaded.id == created.id
    assert repo.count() == 1