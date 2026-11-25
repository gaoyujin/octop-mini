"""Require Bearer JWT on ``/api/*`` except an allowlist."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp

import jwt

from mini.infra.auth.jwt import decode_access_token
from mini.infra.errors import ErrorCode, MiniError

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


def _error_response(code: ErrorCode) -> JSONResponse:
    exc = MiniError(code)
    return JSONResponse(status_code=exc.status, content=exc.to_envelope())


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
            return _error_response(ErrorCode.MISSING_BEARER_TOKEN)

        token = auth[7:].strip()
        try:
            payload = decode_access_token(token)
        except jwt.PyJWTError:
            return _error_response(ErrorCode.INVALID_TOKEN)

        username = str(payload.get("sub") or "")
        runtime = request.app.state.runtime
        if runtime.services is None:
            return _error_response(ErrorCode.DATABASE_NOT_READY)

        row = runtime.services.user_repo.get_by_username(username)
        if row is None:
            return _error_response(ErrorCode.UNKNOWN_USER)

        request.state.mini_user = row
        return await call_next(request)