from __future__ import annotations

from pathlib import Path

import pytest

from mini.infra.boot import boot_control_plane
from mini.infra.config import MiniConfig, load_config
from mini.infra.db.migrate import current_schema_version, run_migrations
from mini.infra.db.factory import open_database
from mini.infra.paths import PathLayout
from mini.infra.runtime import MiniRuntime


def test_migrate_v1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    layout = PathLayout.from_env()
    layout.ensure_root()
    pool = open_database(layout)
    assert current_schema_version(pool) == 0
    version = run_migrations(pool)
    assert version == 4
    assert current_schema_version(pool) == 4
    assert layout.db.is_file()
    version_again = run_migrations(pool)
    assert version_again == 4
    assert current_schema_version(pool) == 4


def test_boot_control_plane(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MINI_HOME", str(tmp_path))
    layout = PathLayout.from_env()
    cfg = load_config(layout=layout)
    runtime = MiniRuntime(layout=layout, config=cfg)
    services = boot_control_plane(runtime)
    assert runtime.database_bound
    assert services.schema_version == 4
    assert services.user_repo.count() == 0