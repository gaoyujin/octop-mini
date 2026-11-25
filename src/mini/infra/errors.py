"""Stable error codes for API boundaries (subset of Octop ``infra/errors``)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ErrorCode(StrEnum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    DATABASE_NOT_READY = "DATABASE_NOT_READY"
    MISSING_BEARER_TOKEN = "MISSING_BEARER_TOKEN"
    INVALID_TOKEN = "INVALID_TOKEN"
    UNKNOWN_USER = "UNKNOWN_USER"
    FORBIDDEN = "FORBIDDEN"
    AGENT_NOT_FOUND = "AGENT_NOT_FOUND"
    AGENT_NAME_TAKEN = "AGENT_NAME_TAKEN"
    AGENT_ALREADY_RUNNING = "AGENT_ALREADY_RUNNING"
    AGENT_NOT_RUNNING = "AGENT_NOT_RUNNING"
    THREAD_NOT_FOUND = "THREAD_NOT_FOUND"


_DEFAULT_STATUS: dict[ErrorCode, int] = {
    ErrorCode.INVALID_CREDENTIALS: 401,
    ErrorCode.NOT_AUTHENTICATED: 401,
    ErrorCode.MISSING_BEARER_TOKEN: 401,
    ErrorCode.INVALID_TOKEN: 401,
    ErrorCode.UNKNOWN_USER: 401,
    ErrorCode.DATABASE_NOT_READY: 503,
    ErrorCode.FORBIDDEN: 403,
    ErrorCode.AGENT_NOT_FOUND: 404,
    ErrorCode.AGENT_NAME_TAKEN: 409,
    ErrorCode.AGENT_ALREADY_RUNNING: 409,
    ErrorCode.AGENT_NOT_RUNNING: 409,
    ErrorCode.THREAD_NOT_FOUND: 404,
}

_DEFAULT_MESSAGES: dict[ErrorCode, str] = {
    ErrorCode.INVALID_CREDENTIALS: "invalid credentials",
    ErrorCode.NOT_AUTHENTICATED: "not authenticated",
    ErrorCode.MISSING_BEARER_TOKEN: "missing bearer token",
    ErrorCode.INVALID_TOKEN: "invalid token",
    ErrorCode.UNKNOWN_USER: "unknown user",
    ErrorCode.DATABASE_NOT_READY: "database not ready",
    ErrorCode.FORBIDDEN: "forbidden",
    ErrorCode.AGENT_NOT_FOUND: "agent not found",
    ErrorCode.AGENT_NAME_TAKEN: "agent name taken",
    ErrorCode.AGENT_ALREADY_RUNNING: "agent already running",
    ErrorCode.AGENT_NOT_RUNNING: "agent not running",
    ErrorCode.THREAD_NOT_FOUND: "thread not found",
}


@dataclass
class MiniError(Exception):
    """Typed domain error mapped to HTTP in ``api/errors``."""

    code: ErrorCode
    message: str = ""
    status: int = 0
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.message:
            self.message = _DEFAULT_MESSAGES[self.code]
        if self.status == 0:
            self.status = _DEFAULT_STATUS[self.code]
        super().__init__(self.message)

    def to_envelope(self) -> dict[str, str]:
        return {"code": self.code.value, "message": self.message}