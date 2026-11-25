"""FastAPI dependencies."""

from __future__ import annotations

from fastapi import HTTPException, Request

from mini.infra.db.repos.users import UserRow
from mini.infra.runtime import MiniRuntime


def get_runtime(request: Request) -> MiniRuntime:
    runtime: MiniRuntime = request.app.state.runtime
    if runtime.services is None:
        raise HTTPException(status_code=503, detail="database not ready")
    return runtime


def current_user(request: Request) -> UserRow:
    user = getattr(request.state, "mini_user", None)
    if user is None:
        raise HTTPException(status_code=401, detail="not authenticated")
    return user