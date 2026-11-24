"""FastAPI factory (HTTP adapter only)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request

if TYPE_CHECKING:
    from mini.infra.runtime import MiniRuntime


def build_app(runtime: MiniRuntime) -> FastAPI:
    """Build the HTTP app for a prepared ``MiniRuntime`` (mirrors ``api/app.build_app``)."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        runtime.mark_started()
        try:
            yield
        finally:
            await runtime.stop()

    app = FastAPI(title="octop-mini", version="0.1.0", lifespan=lifespan)
    app.state.runtime = runtime

    @app.get("/health", summary="Health check")
    async def health(request: Request) -> dict[str, object]:
        rt: MiniRuntime = request.app.state.runtime
        return {
            "ok": True,
            "started": rt.started,
            "mini_home": str(rt.layout.root),
            "bind_host": rt.config.bind_host,
            "port": rt.config.port,
        }

    return app