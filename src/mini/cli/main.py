"""Click root group."""

from __future__ import annotations

import click

from mini.cli.run import run


@click.group()
def cli() -> None:
    """Teaching lab CLI (mirrors ``octop.cli.main`` entry shape)."""


cli.add_command(run)


def main() -> None:
    cli()