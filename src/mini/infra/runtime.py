"""In-process runtime handle (placeholder for future OctopServer equivalent)."""

from __future__ import annotations

from dataclasses import dataclass, field

from mini.infra.config import MiniConfig
from mini.infra.paths import PathLayout


@dataclass(slots=True)
class MiniRuntime:
    """Domain state held for the lifetime of one ``run_foreground`` session."""

    layout: PathLayout
    config: MiniConfig
    _started: bool = field(default=False, repr=False)

    @property
    def started(self) -> bool:
        return self._started

    def mark_started(self) -> None:
        self._started = True

    async def stop(self) -> None:
        """Teardown hook; extend when DB / agents are added."""
        self._started = False