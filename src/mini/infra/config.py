"""Load ``config.json`` with env overrides (M1; aligned with Octop ``load_config``)."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from mini.infra.paths import config_file_path

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class MiniConfig:
    """Subset of Octop bind settings for the teaching lab."""

    bind_host: str = "127.0.0.1"
    port: int = 8765


def _defaults_for_file() -> dict[str, Any]:
    return asdict(MiniConfig())


def env_bind_overrides() -> tuple[str | None, int | None]:
    """Read ``MINI_BIND_HOST`` / ``MINI_PORT`` (same idea as Octop env bind)."""
    host = os.environ.get("MINI_BIND_HOST") or None
    port: int | None = None
    if v := os.environ.get("MINI_PORT"):
        try:
            port = int(v)
        except ValueError:
            logger.warning("env %s is not int; ignoring override", "MINI_PORT")
        if port is not None and not 0 <= port <= 65535:
            logger.warning("env %s is out of range; ignoring override", "MINI_PORT")
            port = None
    return host, port


def _parse_bind_host(raw: dict[str, Any]) -> str | None:
    if "bind_host" in raw and raw["bind_host"] is not None:
        return str(raw["bind_host"])
    if "host" in raw and raw["host"] is not None:
        return str(raw["host"])
    return None


def _parse_port(raw: dict[str, Any]) -> int | None:
    if "port" not in raw or raw["port"] is None:
        return None
    try:
        port = int(raw["port"])
    except (TypeError, ValueError) as exc:
        msg = "config.port must be an integer"
        raise ValueError(msg) from exc
    if not 0 <= port <= 65535:
        msg = "config.port must be between 0 and 65535"
        raise ValueError(msg)
    return port


def load_config(path: Path | None = None) -> MiniConfig:
    """Load ``config.json``; create defaults if missing; apply env overrides last."""
    cfg_path = path if path is not None else config_file_path()
    file_defaults = _defaults_for_file()

    if cfg_path.exists():
        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"{cfg_path} is not valid JSON (line {exc.lineno}, column {exc.colno});"
                " fix it and retry"
            ) from exc
        if not isinstance(raw, dict):
            raise ValueError(
                f"{cfg_path} must contain a JSON object, got {type(raw).__name__}"
            )
    else:
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(json.dumps(file_defaults, indent=2), encoding="utf-8")
        raw = {}

    merged = {**file_defaults, **raw}
    if host := _parse_bind_host(raw):
        merged["bind_host"] = host
    if port := _parse_port(raw):
        merged["port"] = port

    env_host, env_port = env_bind_overrides()
    if env_host is not None:
        merged["bind_host"] = env_host
    if env_port is not None:
        merged["port"] = env_port

    return MiniConfig(
        bind_host=str(merged["bind_host"]),
        port=int(merged["port"]),
    )