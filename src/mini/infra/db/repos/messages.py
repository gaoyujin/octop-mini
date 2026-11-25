"""Chat message rows (course 06)."""

from __future__ import annotations

import time
from dataclasses import dataclass

from mini.infra.db.pool import SqlitePool


@dataclass(frozen=True, slots=True)
class MessageRow:
    id: int
    thread_id: str
    role: str
    content: str
    created_at: int


class MessageRepo:
    def __init__(self, db: SqlitePool) -> None:
        self._db = db

    def append(self, *, thread_id: str, role: str, content: str) -> MessageRow:
        created_at = int(time.time())
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO messages (thread_id, role, content, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (thread_id, role, content, created_at),
            )
            pk = int(cursor.lastrowid)
        return MessageRow(
            id=pk,
            thread_id=thread_id,
            role=role,
            content=content,
            created_at=created_at,
        )

    def list_by_thread(self, thread_id: str) -> list[MessageRow]:
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, thread_id, role, content, created_at
                FROM messages
                WHERE thread_id = ?
                ORDER BY created_at ASC, id ASC
                """,
                (thread_id,),
            ).fetchall()
        return [
            MessageRow(
                id=int(row[0]),
                thread_id=str(row[1]),
                role=str(row[2]),
                content=str(row[3]),
                created_at=int(row[4]),
            )
            for row in rows
        ]