"""Dashboard chat over WebSocket (echo only; course 06)."""

from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from mini.api.common.agent import assert_agent_owner
from mini.api.common.thread import assert_thread_access
from mini.api.deps import resolve_user_from_token
from mini.infra.chat.echo import run_echo_turn
from mini.infra.errors import ErrorCode, MiniError

router = APIRouter()


def _error_frame(exc: MiniError) -> dict[str, str]:
    return {"type": "error", "code": exc.code.value, "message": exc.message}


def _require_running(services: Any, agent_id: str) -> None:
    if not services.agent_manager.is_running(agent_id):
        raise MiniError(ErrorCode.AGENT_NOT_RUNNING)


@router.websocket("/agents/{agent_id}/chat/ws")
async def dashboard_chat_ws(
    websocket: WebSocket,
    agent_id: str,
    token: str | None = Query(default=None),
) -> None:
    """Bidirectional echo chat; authenticate with ``?token=<JWT>``."""
    if not token:
        await websocket.close(code=4001, reason="missing token")
        return

    runtime = websocket.app.state.runtime
    if runtime.services is None:
        await websocket.close(code=4001, reason="database not ready")
        return
    services = runtime.services

    try:
        user = resolve_user_from_token(services, token)
    except MiniError as exc:
        await websocket.close(code=4001, reason=f"auth: {exc.code.value}")
        return

    agent_row = services.agent_repo.get_by_agent_id(agent_id)
    if agent_row is None:
        await websocket.close(code=4004, reason="agent not found")
        return
    try:
        assert_agent_owner(agent_row, user)
    except MiniError:
        await websocket.close(code=4003, reason="forbidden")
        return

    await websocket.accept()

    while True:
        try:
            raw = await websocket.receive_text()
        except WebSocketDisconnect:
            return

        try:
            frame = json.loads(raw)
        except json.JSONDecodeError:
            await websocket.send_json(
                {"type": "error", "code": "INVALID_JSON", "message": "invalid json frame"}
            )
            continue

        if not isinstance(frame, dict) or frame.get("type") != "user_turn":
            await websocket.send_json(
                {
                    "type": "error",
                    "code": "INVALID_FRAME",
                    "message": "expected type user_turn",
                }
            )
            continue

        thread_id = str(frame.get("thread_id") or "")
        text = str(frame.get("text") or "")
        if not thread_id or not text:
            await websocket.send_json(
                {
                    "type": "error",
                    "code": "INVALID_FRAME",
                    "message": "thread_id and text required",
                }
            )
            continue

        try:
            _require_running(services, agent_id)
            thread = services.thread_repo.get_by_thread_id(thread_id)
            if thread is None:
                raise MiniError(ErrorCode.THREAD_NOT_FOUND)
            assert_thread_access(thread, user=user, agent_id=agent_id)
            reply = run_echo_turn(services, thread_id=thread_id, text=text)
        except MiniError as exc:
            await websocket.send_json(_error_frame(exc))
            continue

        await websocket.send_json({"type": "assistant_text", "text": reply})
        await websocket.send_json({"type": "done"})