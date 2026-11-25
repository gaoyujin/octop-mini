"""Agent table access (teaching subset)."""

from __future__ import annotations

import time
from dataclasses import dataclass

from mini.infra.db.pool import SqlitePool


@dataclass(frozen=True, slots=True)
class AgentRow:
    id: int
    agent_id: str
    user_id: int
    name: str
    last_state: str
    created_at: int


class AgentRepo:
    """CRUD helpers; HTTP should reach this via ``SharedServices`` only."""

    def __init__(self, db: SqlitePool) -> None:
        self._db = db

    @staticmethod
    def _row_from_tuple(row: tuple[object, ...]) -> AgentRow:
        return AgentRow(
            id=int(row[0]),
            agent_id=str(row[1]),
            user_id=int(row[2]),
            name=str(row[3]),
            last_state=str(row[4]),
            created_at=int(row[5]),
        )

    def get_by_agent_id(self, agent_id: str) -> AgentRow | None:
        with self._db.connect() as conn:
            row = conn.execute(
                """
                SELECT id, agent_id, user_id, name, last_state, created_at
                FROM agents WHERE agent_id = ?
                """,
                (agent_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_from_tuple(row)

    def list_by_user_id(self, user_id: int) -> list[AgentRow]:
        with self._db.connect() as conn:
            rows = conn.execute(
                """
                SELECT id, agent_id, user_id, name, last_state, created_at
                FROM agents WHERE user_id = ?
                ORDER BY created_at ASC
                """,
                (user_id,),
            ).fetchall()
        return [self._row_from_tuple(row) for row in rows]

    def create(
        self,
        *,
        agent_id: str,
        user_id: int,
        name: str,
        last_state: str = "stopped",
    ) -> AgentRow:
        created_at = int(time.time())
        with self._db.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO agents (agent_id, user_id, name, last_state, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (agent_id, user_id, name, last_state, created_at),
            )
            pk = int(cursor.lastrowid)
        return AgentRow(
            id=pk,
            agent_id=agent_id,
            user_id=user_id,
            name=name,
            last_state=last_state,
            created_at=created_at,
        )

    def set_last_state(self, agent_id: str, last_state: str) -> AgentRow | None:
        with self._db.connect() as conn:
            conn.execute(
                "UPDATE agents SET last_state = ? WHERE agent_id = ?",
                (last_state, agent_id),
            )
        return self.get_by_agent_id(agent_id)

    def count(self) -> int:
        with self._db.connect() as conn:
            row = conn.execute("SELECT COUNT(*) FROM agents").fetchone()
        return int(row[0]) if row is not None else 0