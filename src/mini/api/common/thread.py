"""Thread access checks for HTTP and WebSocket."""

from __future__ import annotations

from mini.infra.db.repos.threads import ThreadRow
from mini.infra.db.repos.users import UserRow
from mini.infra.errors import ErrorCode, MiniError


def assert_thread_access(thread: ThreadRow, *, user: UserRow, agent_id: str) -> None:
    """Raise if the thread does not belong to this user and agent."""
    if thread.agent_id != agent_id or thread.user_id != user.id:
        raise MiniError(ErrorCode.THREAD_NOT_FOUND)