"""Agent lifecycle (mock harness; course 05)."""

from __future__ import annotations

import secrets
import sqlite3

from mini.infra.agents.workspace import init_agent_workspace
from mini.infra.db.repos.agents import AgentRepo, AgentRow
from mini.infra.errors import ErrorCode, MiniError
from mini.infra.paths import PathLayout

_STATE_STOPPED = "stopped"
_STATE_RUNNING = "running"


class AgentManager:
    """Create agents, track mock running ids in memory."""

    def __init__(self, agents: AgentRepo, layout: PathLayout) -> None:
        self._agents = agents
        self._layout = layout
        self._running: set[str] = set()

    def is_running(self, agent_id: str) -> bool:
        return agent_id in self._running

    def list_for_user(self, user_id: int) -> list[AgentRow]:
        return self._agents.list_by_user_id(user_id)

    def create_agent(self, *, user_id: int, name: str) -> AgentRow:
        agent_id = f"ag_{secrets.token_hex(8)}"
        try:
            row = self._agents.create(agent_id=agent_id, user_id=user_id, name=name)
        except sqlite3.IntegrityError as exc:
            raise MiniError(ErrorCode.AGENT_NAME_TAKEN) from exc
        init_agent_workspace(self._layout, agent_id)
        return row

    def start_agent(self, agent_id: str) -> AgentRow:
        row = self._require_agent(agent_id)
        if agent_id in self._running:
            raise MiniError(ErrorCode.AGENT_ALREADY_RUNNING)
        self._running.add(agent_id)
        updated = self._agents.set_last_state(agent_id, _STATE_RUNNING)
        assert updated is not None
        return updated

    def stop_agent(self, agent_id: str) -> AgentRow:
        self._require_agent(agent_id)
        if agent_id not in self._running:
            raise MiniError(ErrorCode.AGENT_NOT_RUNNING)
        self._running.discard(agent_id)
        updated = self._agents.set_last_state(agent_id, _STATE_STOPPED)
        assert updated is not None
        return updated

    def _require_agent(self, agent_id: str) -> AgentRow:
        row = self._agents.get_by_agent_id(agent_id)
        if row is None:
            raise MiniError(ErrorCode.AGENT_NOT_FOUND)
        return row