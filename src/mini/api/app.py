"""FastAPI factory (HTTP adapter only)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI

from mini.api.errors import register_exception_handlers
from mini.api.middleware.jwt_auth import install_jwt_auth
from mini.api.openapi_meta import OPENAPI_TAGS
from mini.api.routers import agents, auth, health, settings, threads
from mini.api.routers.chat import ws as chat_ws

if TYPE_CHECKING:
    from mini.infra.runtime import MiniRuntime


def build_app(runtime: MiniRuntime) -> FastAPI:
    """Assemble routers, middleware, and handlers for a prepared ``MiniRuntime``."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        runtime.mark_started()
        try:
            yield
        finally:
            await runtime.stop()

    app = FastAPI(
        title="octop-mini",
        version="0.1.0",
        lifespan=lifespan,
        openapi_tags=OPENAPI_TAGS,
    )
    app.state.runtime = runtime
    register_exception_handlers(app)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(settings.router)
    app.include_router(agents.router)
    app.include_router(threads.router)
    app.include_router(chat_ws.router, prefix="/api")
    install_jwt_auth(app)
    return app