"""JWT sign/verify (teaching subset)."""

from __future__ import annotations

import os
import time
from typing import Any

import jwt

_DEFAULT_TTL_SECONDS = 86400


def jwt_secret() -> str:
    secret = os.environ.get("MINI_JWT_SECRET", "").strip()
    if secret:
        return secret
    return "octop-mini-dev-secret-change-me-32b-min"


def create_access_token(*, username: str, ttl_seconds: int = _DEFAULT_TTL_SECONDS) -> str:
    now = int(time.time())
    payload = {
        "sub": username,
        "iat": now,
        "exp": now + ttl_seconds,
    }
    return jwt.encode(payload, jwt_secret(), algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, jwt_secret(), algorithms=["HS256"])