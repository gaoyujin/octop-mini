"""``octop-mini run`` — resolve bind, then hand off to ``launch``."""

from __future__ import annotations

import click

from mini.cli.bind import resolve_bind, save_configfile_overrides


def _run_uvicorn(**kwargs: object) -> None:
    """Indirection seam for tests; production runs uvicorn via ``launch``."""
    from mini.launch import run_foreground_blocking

    run_foreground_blocking(**kwargs)


@click.command("run")
@click.option("--host", default=None, help="Override bind host")
@click.option("--port", default=None, type=click.IntRange(0, 65535), help="Override port")
@click.option("--reload", is_flag=True, default=False, help="Enable uvicorn auto-reload (dev).")
@click.option("--workers", default=1, type=int, help="Worker process count (default 1).")
@click.option(
    "--log-level",
    type=click.Choice(["critical", "error", "warning", "info", "debug"], case_sensitive=False),
    default=None,
)
def run(
    host: str | None,
    port: int | None,
    reload: bool,
    workers: int,
    log_level: str | None,
) -> None:
    """Run octop-mini in the foreground (CLI layer only — no uvicorn here)."""
    cli_host, cli_port = host, port
    host, port = resolve_bind(host, port)
    if cli_host is not None or cli_port is not None:
        path = save_configfile_overrides(cli_host, cli_port)
        click.echo(f"Saved config to {path}")
    _run_uvicorn(
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_level=log_level,
    )