"""``OctopServer.start()`` first segment — open DB, migrate, services."""

from __future__ import annotations

import logging

from mini.infra.db.factory import open_database
from mini.infra.db.migrate import run_migrations
from mini.infra.db.services import SharedServices, build_shared_services
from mini.infra.runtime import MiniRuntime

logger = logging.getLogger(__name__)


def boot_control_plane(runtime: MiniRuntime) -> SharedServices:
    """Open sqlite, migrate, attach ``SharedServices`` to runtime."""
    runtime.layout.ensure_root()
    pool = open_database(runtime.layout)
    version = run_migrations(pool)
    services = build_shared_services(
        db=pool,
        layout=runtime.layout,
        config=runtime.config,
    )
    runtime.attach_services(services)
    logger.info(
        "Control plane ready db=%s schema_version=%s",
        runtime.layout.db,
        version,
    )
    return services