"""OpenAPI tag metadata for ``/docs``."""

from __future__ import annotations

from typing import Any

OPENAPI_TAGS: list[dict[str, Any]] = [
    {"name": "health", "description": "Liveness probe (no auth)."},
    {"name": "auth", "description": "Login and current user."},
    {"name": "settings", "description": "Read-only server bind settings (JWT required)."},
    {"name": "agents", "description": "Agent CRUD and mock start/stop (JWT + ownership)."},
]