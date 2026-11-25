"""Liveness probe (no auth)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from mini.api.deps import get_runtime_handle
from mini.infra.runtime import MiniRuntime

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    ok: bool
    started: bool
    db_bound: bool
    schema_version: int | None
    users_loaded: int
    mini_home: str
    bind_host: str
    port: int


@router.get("/health", response_model=HealthResponse, summary="Health check")
def health(runtime: MiniRuntime = Depends(get_runtime_handle)) -> HealthResponse:
    """Process liveness and DB migration watermark (public)."""
    services = runtime.services
    version = services.schema_version if services is not None else None
    users_loaded = services.user_repo.count() if services is not None else 0
    return HealthResponse(
        ok=True,
        started=runtime.started,
        db_bound=runtime.database_bound,
        schema_version=version,
        users_loaded=users_loaded,
        mini_home=str(runtime.layout.root),
        bind_host=runtime.config.bind_host,
        port=runtime.config.port,
    )