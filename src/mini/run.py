"""Backward-compatible entry: ``uv run octop-mini`` → Click CLI."""

from __future__ import annotations

from mini.cli.main import main

__all__ = ["main"]

if __name__ == "__main__":
    main()