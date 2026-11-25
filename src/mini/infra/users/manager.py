"""User authentication (mirrors ``infra/users/manager`` surface)."""

from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from mini.infra.db.repos.users import UserRepo, UserRow

_hasher = PasswordHasher()


class UserManager:
    def __init__(self, users: UserRepo) -> None:
        self._users = users

    def hash_password(self, password: str) -> str:
        return _hasher.hash(password)

    def verify_password(self, password_hash: str, password: str) -> bool:
        try:
            return _hasher.verify(password_hash, password)
        except VerifyMismatchError:
            return False

    def create_user(self, username: str, password: str) -> UserRow:
        password_hash = self.hash_password(password)
        return self._users.create(username=username, password_hash=password_hash)

    def authenticate(self, username: str, password: str) -> UserRow | None:
        row = self._users.get_by_username(username)
        if row is None or not row.password_hash:
            return None
        if not self.verify_password(row.password_hash, password):
            return None
        return row