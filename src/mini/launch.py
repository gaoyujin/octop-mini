"""Composition root — wire ``MiniRuntime``, FastAPI, and uvicorn."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import replace
from typing import Any

import uvicorn

from mini.api.app import build_app
from mini.infra.config import MiniConfig, load_config
from mini.infra.paths import PathLayout
from mini.infra.runtime import MiniRuntime

logger = logging.getLogger(__name__)


async def run_foreground(
    *,
    host: str | None,
    port: int | None,
    reload: bool,
    workers: int,
    log_level: str | None,
    ssl_certfile: str | None = None,
    ssl_keyfile: str | None = None,
) -> None:
    """Boot runtime, serve HTTP, then shut down cleanly."""
    if ssl_certfile or ssl_keyfile:
        logger.warning("TLS is not implemented in octop-mini; ignoring ssl options")

    layout = PathLayout.from_env()
    layout.ensure_root()
    cfg = load_config(layout=layout)

    bind_host = host if host is not None else cfg.bind_host
    bind_port = port if port is not None else cfg.port
    effective = replace(cfg, bind_host=bind_host, port=bind_port)
    # 组合根：绑定本次 run 会话的路径布局与生效配置（后续 DB/agent 等也挂在此对象上）
    runtime = MiniRuntime(layout=layout, config=effective)

    # uvicorn 日志级别；reload 模式下只能单进程，否则取 CLI 的 workers（至少 1）
    level = (log_level or "info").lower()
    worker_count = 1 if reload else max(1, workers)

    # 用同一 runtime 构建 FastAPI，并写入 app.state 供路由与 lifespan 使用
    app = build_app(runtime)
    config = uvicorn.Config(
        app,
        host=bind_host,
        port=bind_port,
        log_level=level,
        workers=worker_count,
        reload=reload,
    )
    server = uvicorn.Server(config)

    logger.info("Listening on http://%s:%s (mini_home=%s)", bind_host, bind_port, layout.root)
    try:
        await server.serve()
    finally:
        await runtime.stop()


def run_foreground_blocking(**kwargs: Any) -> None:
    """Sync entry for Click commands and tests."""
    asyncio.run(run_foreground(**kwargs))