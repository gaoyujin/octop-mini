"""DI container after DB is open (subset of ``build_shared_services``)."""

from __future__ import annotations

from dataclasses import dataclass

from mini.infra.config import MiniConfig
from mini.infra.db.migrate import current_schema_version
from mini.infra.db.pool import SqlitePool
from mini.infra.db.repos.users import UserRepo
from mini.infra.paths import PathLayout


@dataclass(frozen=True, slots=True)
class SharedServices:
    """DI container: repos hang here; HTTP reaches data via ``runtime.services``."""

    db: SqlitePool
    layout: PathLayout
    config: MiniConfig
    user_repo: UserRepo

    @property
    def schema_version(self) -> int:
        return current_schema_version(self.db)


def build_shared_services(
    *,
    db: SqlitePool,
    layout: PathLayout,
    config: MiniConfig,
) -> SharedServices:
    return SharedServices(
        db=db,
        layout=layout,
        config=config,
        user_repo=UserRepo(db),
    )