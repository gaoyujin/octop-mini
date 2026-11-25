"""FastAPI dependencies."""

from __future__ import annotations

from fastapi import Depends, Request

from mini.infra.db.repos.users import UserRow
from mini.infra.db.services import SharedServices
from mini.infra.errors import ErrorCode, MiniError
from mini.infra.runtime import MiniRuntime


def get_runtime_handle(request: Request) -> MiniRuntime:
    """Runtime from app state (health may run before DB is bound)."""
    return request.app.state.runtime


def get_runtime(runtime: MiniRuntime = Depends(get_runtime_handle)) -> MiniRuntime:
    if runtime.services is None:
        raise MiniError(ErrorCode.DATABASE_NOT_READY)
    return runtime


def get_services(runtime: MiniRuntime = Depends(get_runtime)) -> SharedServices:
    """Shared repos/managers for thin routers."""
    services = runtime.services
    assert services is not None
    return services


def current_user(request: Request) -> UserRow:
    user = getattr(request.state, "mini_user", None)
    if user is None:
        raise MiniError(ErrorCode.NOT_AUTHENTICATED)
    return user