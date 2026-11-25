"""User table access (teaching subset)."""

from __future__ import annotations

import time
from dataclasses import dataclass

from mini.infra.db.pool import SqlitePool


@dataclass(frozen=True, slots=True)
class UserRow:
    id: int
    username: str
    created_at: int
    password_hash: str | None = None


class UserRepo:
    """CRUD helpers; HTTP should reach this via ``SharedServices`` only."""

    def __init__(self, db: SqlitePool) -> None:
        self._db = db

    def get_by_username(self, username: str) -> UserRow | None:
        with self._db.connect() as conn:
            row = conn.execute(
                "SELECT id, username, created_at, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()
        if row is None:
            return None
        return UserRow(
            id=int(row[0]),
            username=str(row[1]),
            created_at=int(row[2]),
            password_hash=str(row[3]) if row[3] is not None else None,
        )

    def create(self, *, username: str, password_hash: str) -> UserRow:
        created_at = int(time.time())
        with self._db.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, created_at, password_hash) VALUES (?, ?, ?)",
                (username, created_at, password_hash),
            )
            user_id = int(cursor.lastrowid)
        return UserRow(
            id=user_id,
            username=username,
            created_at=created_at,
            password_hash=password_hash,
        )

    def count(self) -> int:
        with self._db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
        return int(row[0]) if row is not None else 0