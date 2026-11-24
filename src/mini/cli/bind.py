"""Bind address resolution (CLI > env > config.json)."""

from __future__ import annotations

import json
from pathlib import Path

from mini.infra.config import env_bind_overrides
from mini.infra.paths import PathLayout


def _load_configfile_overrides() -> tuple[str | None, int | None]:
    cfg_path = PathLayout.from_env().config
    if not cfg_path.exists():
        return None, None
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{cfg_path} is not valid JSON (line {exc.lineno}, column {exc.colno})"
        ) from exc
    if not isinstance(data, dict):
        return None, None
    host = data.get("bind_host") or data.get("host")
    port = data.get("port")
    return (
        host if isinstance(host, str) else None,
        port if isinstance(port, int) and not isinstance(port, bool) else None,
    )


def resolve_bind(host: str | None, port: int | None) -> tuple[str | None, int | None]:
    """CLI flag > ``MINI_*`` env > ``config.json``."""
    cfg_host, cfg_port = _load_configfile_overrides()
    env_host, env_port = env_bind_overrides()
    resolved_host = host if host is not None else env_host if env_host is not None else cfg_host
    resolved_port = port if port is not None else env_port if env_port is not None else cfg_port
    return resolved_host, resolved_port


def save_configfile_overrides(host: str | None, port: int | None) -> Path:
    """Merge host/port into ``config.json`` when CLI explicitly overrides."""
    paths = PathLayout.from_env()
    paths.ensure_root()
    cfg_path = paths.config
    if cfg_path.exists():
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{cfg_path} must contain a JSON object")
    else:
        data = {}
    if host is not None:
        data["bind_host"] = host
    if port is not None:
        data["port"] = port
    cfg_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return cfg_path