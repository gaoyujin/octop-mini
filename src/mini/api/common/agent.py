"""Agent ownership checks for HTTP routers."""

from __future__ import annotations

from mini.infra.db.repos.agents import AgentRow
from mini.infra.db.repos.users import UserRow
from mini.infra.errors import ErrorCode, MiniError


def assert_agent_owner(row: AgentRow, user: UserRow) -> None:
    """Raise if the agent row belongs to another user."""
    if row.user_id != user.id:
        raise MiniError(ErrorCode.FORBIDDEN, message="agent not owned by user")