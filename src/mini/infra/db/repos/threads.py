"""Thread table access (course 06)."""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass

from mini.infra.db.pool import SqlitePool

_DASHBOARD_CHANNEL = "dashboard"
_DEFAULT_TITLE = "New chat"


@dataclass(frozen=True, slots=True)
class ThreadRow:
    id: int
    thread_id: str
    agent_id: str
    user_id: int
    channel_type: str
    session_key: str
    title: str | None
    last_active: int
    created_at: int


class ThreadRepo:
    def __init__(self, db: SqlitePool) -> None:
        self._db = db

    @staticmethod
    def _row_from_tuple(row: tuple[object, ...]) -> ThreadRow:
        return ThreadRow(
            id=int(row[0]),
            thread_id=str(row[1]),
            agent_id=str(row[2]),
            user_id=int(row[3]),
            channel_type=str(row[4]),
            session_key=str(row[5]),
            title=str(row[6]) if row[6] is not None else None,
            last_active=int(row[7]),
            created_at=int(row[8]),
        )

    def _select_columns(self) -> str:
        return """
            id, thread_id, agent_id, user_id, channel_type,
            session_key, title, last_active, created_at
        """

    def get_by_thread_id(self, thread_id: str) -> ThreadRow | None:
        with self._db.connect() as conn:
            row = conn.execute(
                f"""
                SELECT {self._select_columns()}
                FROM threads WHERE thread_id = ?
                """,
                (thread_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_from_tuple(row)

    def list_by_agent_and_user(self, *, agent_id: str, user_id: int) -> list[ThreadRow]:
        with self._db.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT {self._select_columns()}
                FROM threads
                WHERE agent_id = ? AND user_id = ?
                ORDER BY last_active DESC
                """,
                (agent_id, user_id),
            ).fetchall()
        return [self._row_from_tuple(row) for row in rows]

    def create(
        self,
        *,
        agent_id: str,
        user_id: int,
        title: str | None = None,
    ) -> ThreadRow:
        thread_id = f"th_{secrets.token_hex(8)}"
        session_key = f"dashboard:{agent_id}:{thread_id}"
        now = int(time.time())
        resolved_title = title if title else _DEFAULT_TITLE
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO threads (
                    thread_id, agent_id, user_id, channel_type,
                    session_key, title, last_active, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    thread_id,
                    agent_id,
                    user_id,
                    _DASHBOARD_CHANNEL,
                    session_key,
                    resolved_title,
                    now,
                    now,
                ),
            )
            pk = int(cursor.lastrowid)
        return ThreadRow(
            id=pk,
            thread_id=thread_id,
            agent_id=agent_id,
            user_id=user_id,
            channel_type=_DASHBOARD_CHANNEL,
            session_key=session_key,
            title=resolved_title,
            last_active=now,
            created_at=now,
        )

    def touch_last_active(self, thread_id: str) -> None:
        now = int(time.time())
        with self._db.connect() as conn:
            conn.execute(
                "UPDATE threads SET last_active = ? WHERE thread_id = ?",
                (now, thread_id),
            )