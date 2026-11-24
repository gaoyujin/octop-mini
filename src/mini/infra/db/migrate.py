"""Apply numbered ``NNN_*.sql`` migrations."""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from mini.infra.db.pool import SqlitePool

_MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _discover() -> list[tuple[int, Path]]:
    out: list[tuple[int, Path]] = []
    if not _MIGRATIONS_DIR.is_dir():
        return out
    for entry in sorted(_MIGRATIONS_DIR.iterdir()):
        match = re.match(r"^(\d{3})_.*\.sql$", entry.name)
        if match and not entry.name.endswith(".pg.sql"):
            out.append((int(match.group(1)), entry))
    return out


def current_schema_version(db: SqlitePool) -> int:
    with db.connect() as conn:
        try:
            row = conn.execute("SELECT version FROM _schema_version").fetchone()
        except sqlite3.OperationalError:
            return 0
        if row is None:
            return 0
        return int(row[0])


def run_migrations(db: SqlitePool) -> int:
    """Apply pending migrations; return final schema version."""
    current = current_schema_version(db)
    latest = current
    for version, path in _discover():
        if version <= current:
            continue
        sql = path.read_text(encoding="utf-8")
        with db.connect() as conn:
            conn.executescript(sql)
        latest = version
    return latest