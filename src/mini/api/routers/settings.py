"""Read-only settings routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from mini.api.deps import current_user, get_runtime
from mini.infra.db.repos.users import UserRow
from mini.infra.runtime import MiniRuntime

router = APIRouter(prefix="/api/settings", tags=["settings"])


class BindSettingsResponse(BaseModel):
    bind_host: str
    port: int


@router.get(
    "/bind",
    response_model=BindSettingsResponse,
    summary="HTTP bind host and port",
)
def read_bind(
    _user: UserRow = Depends(current_user),
    runtime: MiniRuntime = Depends(get_runtime),
) -> BindSettingsResponse:
    """Return listen address from ``config.json`` (requires JWT)."""
    return BindSettingsResponse(
        bind_host=runtime.config.bind_host,
        port=runtime.config.port,
    )