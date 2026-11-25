"""Login routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from mini.api.deps import current_user, get_runtime
from mini.infra.auth.jwt import create_access_token
from mini.infra.db.repos.users import UserRow
from mini.infra.runtime import MiniRuntime

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginBody(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    username: str


@router.post("/login", response_model=LoginResponse, summary="Login")
def login(body: LoginBody, runtime: MiniRuntime = Depends(get_runtime)) -> LoginResponse:
    user = runtime.services.user_manager.authenticate(body.username, body.password)
    if user is None:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token(username=user.username)
    return LoginResponse(access_token=token)


@router.get("/me", response_model=MeResponse, summary="Current user")
def me(user: UserRow = Depends(current_user)) -> MeResponse:
    return MeResponse(id=user.id, username=user.username)