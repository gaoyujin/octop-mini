"""DI container after DB is open (subset of ``build_shared_services``)."""

from __future__ import annotations

from dataclasses import dataclass

from mini.infra.config import MiniConfig
from mini.infra.db.migrate import current_schema_version
from mini.infra.db.pool import SqlitePool
from mini.infra.agents.manager import AgentManager
from mini.infra.db.repos.agents import AgentRepo
from mini.infra.db.repos.messages import MessageRepo
from mini.infra.db.repos.threads import ThreadRepo
from mini.infra.db.repos.users import UserRepo
from mini.infra.paths import PathLayout
from mini.infra.users.manager import UserManager


@dataclass(frozen=True, slots=True)
class SharedServices:
    """DI container: repos hang here; HTTP reaches data via ``runtime.services``."""

    db: SqlitePool
    layout: PathLayout
    config: MiniConfig
    user_repo: UserRepo
    user_manager: UserManager
    agent_repo: AgentRepo
    agent_manager: AgentManager
    thread_repo: ThreadRepo
    message_repo: MessageRepo

    @property
    def schema_version(self) -> int:
        return current_schema_version(self.db)


def build_shared_services(
    *,
    db: SqlitePool,
    layout: PathLayout,
    config: MiniConfig,
) -> SharedServices:
    user_repo = UserRepo(db)
    agent_repo = AgentRepo(db)
    thread_repo = ThreadRepo(db)
    message_repo = MessageRepo(db)
    return SharedServices(
        db=db,
        layout=layout,
        config=config,
        user_repo=user_repo,
        user_manager=UserManager(user_repo),
        agent_repo=agent_repo,
        agent_manager=AgentManager(agent_repo, layout),
        thread_repo=thread_repo,
        message_repo=message_repo,
    )