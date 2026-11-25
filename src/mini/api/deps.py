"""FastAPI dependencies."""

from __future__ import annotations

import jwt
from fastapi import Depends, Request

from mini.infra.auth.jwt import decode_access_token
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


def resolve_user_from_token(services: SharedServices, token: str) -> UserRow:
    """WebSocket auth: query ``?token=`` mirrors official ``resolve_user_from_token``."""
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError as exc:
        raise MiniError(ErrorCode.INVALID_TOKEN) from exc
    username = str(payload.get("sub") or "")
    row = services.user_repo.get_by_username(username)
    if row is None:
        raise MiniError(ErrorCode.UNKNOWN_USER)
    return row