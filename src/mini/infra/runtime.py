"""In-process runtime handle (mini ``OctopServer``)."""

from __future__ import annotations

from dataclasses import dataclass, field

from mini.infra.config import MiniConfig
from mini.infra.db.services import SharedServices
from mini.infra.paths import PathLayout


@dataclass(slots=True)
class MiniRuntime:
    """Domain state held for the lifetime of one ``run_foreground`` session."""

    layout: PathLayout
    config: MiniConfig
    services: SharedServices | None = None
    _started: bool = field(default=False, repr=False)

    @property
    def started(self) -> bool:
        return self._started

    @property
    def database_bound(self) -> bool:
        return self.services is not None

    def attach_services(self, services: SharedServices) -> None:
        self.services = services

    def mark_started(self) -> None:
        self._started = True

    async def stop(self) -> None:
        if self.services is not None:
            self.services.db.close()
        self.services = None
        self._started = False