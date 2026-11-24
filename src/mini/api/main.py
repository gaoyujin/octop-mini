"""Default ASGI app for ``uvicorn mini.api.main:app`` and unit tests."""

from __future__ import annotations

from mini.api.app import build_app
from mini.infra.boot import boot_control_plane
from mini.infra.config import load_config
from mini.infra.paths import PathLayout
from mini.infra.runtime import MiniRuntime


def _dev_runtime() -> MiniRuntime:
    layout = PathLayout.from_env()
    layout.ensure_root()
    cfg = load_config(layout=layout)
    runtime = MiniRuntime(layout=layout, config=cfg)
    boot_control_plane(runtime)
    return runtime


app = build_app(_dev_runtime())