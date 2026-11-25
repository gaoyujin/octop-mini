"""Map ``MiniError`` to HTTP responses."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from mini.infra.errors import MiniError


def register_exception_handlers(app: FastAPI) -> None:
    """Install the global ``MiniError`` handler."""

    @app.exception_handler(MiniError)
    async def _mini_error(_request: Request, exc: MiniError) -> JSONResponse:
        return JSONResponse(status_code=exc.status, content=exc.to_envelope())