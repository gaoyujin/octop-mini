"""Agent CRUD and mock start/stop (course 05)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from mini.api.common.agent import assert_agent_owner
from mini.api.deps import current_user, get_services
from mini.infra.db.repos.users import UserRow
from mini.infra.db.services import SharedServices
from mini.infra.errors import ErrorCode, MiniError

router = APIRouter(prefix="/api/agents", tags=["agents"])


class CreateAgentBody(BaseModel):
    name: str = Field(min_length=1, max_length=128)


class AgentItem(BaseModel):
    agent_id: str
    name: str
    last_state: str


class AgentListResponse(BaseModel):
    agents: list[AgentItem]


class AgentStateResponse(BaseModel):
    agent_id: str
    state: str


def _load_owned_agent(
    agent_id: str,
    user: UserRow,
    services: SharedServices,
) -> None:
    row = services.agent_repo.get_by_agent_id(agent_id)
    if row is None:
        raise MiniError(ErrorCode.AGENT_NOT_FOUND)
    assert_agent_owner(row, user)


@router.get("", response_model=AgentListResponse, summary="List my agents")
def list_agents(
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> AgentListResponse:
    rows = services.agent_manager.list_for_user(user.id)
    return AgentListResponse(
        agents=[
            AgentItem(agent_id=r.agent_id, name=r.name, last_state=r.last_state)
            for r in rows
        ]
    )


@router.post("", response_model=AgentItem, summary="Create an agent")
def create_agent(
    body: CreateAgentBody,
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> AgentItem:
    row = services.agent_manager.create_agent(user_id=user.id, name=body.name)
    return AgentItem(agent_id=row.agent_id, name=row.name, last_state=row.last_state)


@router.post(
    "/{agent_id}/start",
    response_model=AgentStateResponse,
    summary="Start agent (mock)",
)
def start_agent(
    agent_id: str,
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> AgentStateResponse:
    _load_owned_agent(agent_id, user, services)
    row = services.agent_manager.start_agent(agent_id)
    return AgentStateResponse(agent_id=row.agent_id, state=row.last_state)


@router.post(
    "/{agent_id}/stop",
    response_model=AgentStateResponse,
    summary="Stop agent (mock)",
)
def stop_agent(
    agent_id: str,
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> AgentStateResponse:
    _load_owned_agent(agent_id, user, services)
    row = services.agent_manager.stop_agent(agent_id)
    return AgentStateResponse(agent_id=row.agent_id, state=row.last_state)