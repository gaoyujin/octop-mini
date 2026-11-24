"""Open the control-plane SQLite file."""

from __future__ import annotations

from mini.infra.db.pool import SqlitePool
from mini.infra.paths import PathLayout


def open_database(paths: PathLayout) -> SqlitePool:
    """Return a pool for ``paths.db`` (mirrors ``open_database(config, paths)``)."""
    return SqlitePool(paths.db)