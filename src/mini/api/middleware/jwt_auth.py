"""Require Bearer JWT on ``/api/*`` except an allowlist."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp

import jwt

from mini.infra.auth.jwt import decode_access_token
from mini.infra.db.repos.users import UserRow

_JWT_EXEMPT_EXACT = frozenset(
    {
        "/api/auth/login",
        "/openapi.json",
        "/docs",
        "/redoc",
    }
)


def is_jwt_exempt(path: str) -> bool:
    return path in _JWT_EXEMPT_EXACT


def install_jwt_auth(app: ASGIApp) -> None:
    @app.middleware("http")
    async def _jwt_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        path = request.url.path
        if not path.startswith("/api/") or is_jwt_exempt(path):
            return await call_next(request)

        auth = request.headers.get("authorization") or ""
        if not auth.lower().startswith("bearer "):
            return JSONResponse(status_code=401, content={"detail": "missing bearer token"})

        token = auth[7:].strip()
        try:
            payload = decode_access_token(token)
        except jwt.PyJWTError:
            return JSONResponse(status_code=401, content={"detail": "invalid token"})

        username = str(payload.get("sub") or "")
        runtime = request.app.state.runtime
        if runtime.services is None:
            return JSONResponse(status_code=503, content={"detail": "database not ready"})

        row = runtime.services.user_repo.get_by_username(username)
        if row is None:
            return JSONResponse(status_code=401, content={"detail": "unknown user"})

        request.state.mini_user = row
        return await call_next(request)