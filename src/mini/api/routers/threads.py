"""Thread list/create and message history."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from mini.api.common.agent import assert_agent_owner
from mini.api.common.thread import assert_thread_access
from mini.api.deps import current_user, get_services
from mini.infra.db.repos.users import UserRow
from mini.infra.db.services import SharedServices
from mini.infra.errors import ErrorCode, MiniError

router = APIRouter(prefix="/api/agents", tags=["threads"])


class CreateThreadBody(BaseModel):
    title: str | None = Field(default=None, max_length=256)


class ThreadItem(BaseModel):
    thread_id: str
    title: str | None
    session_key: str
    last_active: int


class ThreadListResponse(BaseModel):
    threads: list[ThreadItem]


class MessageItem(BaseModel):
    role: str
    content: str
    created_at: int


class MessageListResponse(BaseModel):
    messages: list[MessageItem]


def _load_owned_agent(agent_id: str, user: UserRow, services: SharedServices) -> None:
    row = services.agent_repo.get_by_agent_id(agent_id)
    if row is None:
        raise MiniError(ErrorCode.AGENT_NOT_FOUND)
    assert_agent_owner(row, user)


def _load_thread(
    thread_id: str,
    agent_id: str,
    user: UserRow,
    services: SharedServices,
) -> None:
    thread = services.thread_repo.get_by_thread_id(thread_id)
    if thread is None:
        raise MiniError(ErrorCode.THREAD_NOT_FOUND)
    assert_thread_access(thread, user=user, agent_id=agent_id)


@router.get(
    "/{agent_id}/threads",
    response_model=ThreadListResponse,
    summary="List chat threads for an agent",
)
def list_threads(
    agent_id: str,
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> ThreadListResponse:
    _load_owned_agent(agent_id, user, services)
    rows = services.thread_repo.list_by_agent_and_user(agent_id=agent_id, user_id=user.id)
    return ThreadListResponse(
        threads=[
            ThreadItem(
                thread_id=r.thread_id,
                title=r.title,
                session_key=r.session_key,
                last_active=r.last_active,
            )
            for r in rows
        ]
    )


@router.post(
    "/{agent_id}/threads",
    response_model=ThreadItem,
    summary="Create a chat thread",
)
def create_thread(
    agent_id: str,
    body: CreateThreadBody,
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> ThreadItem:
    _load_owned_agent(agent_id, user, services)
    row = services.thread_repo.create(
        agent_id=agent_id,
        user_id=user.id,
        title=body.title,
    )
    return ThreadItem(
        thread_id=row.thread_id,
        title=row.title,
        session_key=row.session_key,
        last_active=row.last_active,
    )


@router.get(
    "/{agent_id}/threads/{thread_id}/messages",
    response_model=MessageListResponse,
    summary="List messages in a thread",
)
def list_messages(
    agent_id: str,
    thread_id: str,
    user: UserRow = Depends(current_user),
    services: SharedServices = Depends(get_services),
) -> MessageListResponse:
    _load_owned_agent(agent_id, user, services)
    _load_thread(thread_id, agent_id, user, services)
    rows = services.message_repo.list_by_thread(thread_id)
    return MessageListResponse(
        messages=[
            MessageItem(role=r.role, content=r.content, created_at=r.created_at)
            for r in rows
        ]
    )