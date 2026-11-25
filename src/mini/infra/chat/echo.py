"""Mock chat turn: persist user text and echo assistant reply."""

from __future__ import annotations

from mini.infra.db.services import SharedServices


def run_echo_turn(services: SharedServices, *, thread_id: str, text: str) -> str:
    """Store user + assistant rows; bump thread ``last_active``."""
    services.message_repo.append(thread_id=thread_id, role="user", content=text)
    reply = f"echo: {text}"
    services.message_repo.append(thread_id=thread_id, role="assistant", content=reply)
    services.thread_repo.touch_last_active(thread_id)
    return reply