from datetime import UTC, datetime
from typing import Protocol

from core.either import Either, Left, Right
from domain.auth.enterprise.entities.user import User
from domain.auth.roles import ALL_ROLES, ROLE_ADMIN, ROLE_VIEWER
from domain.runops.application.errors.not_allowed_error import NotAllowedError
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError


class UsersRepository(Protocol):
    async def find_by_id(self, user_id: str) -> User | None: ...
    async def list_all(self) -> list[User]: ...
    async def save(self, user: User) -> None: ...


class ResolveUserUseCase:
    """Authorization lives in Cloud Wise: a first login registers the user as viewer
    (or admin, if the email is listed in ADMIN_EMAILS)."""

    def __init__(self, users: UsersRepository, admin_emails: list[str]) -> None:
        self._users = users
        self._admin_emails = {e.strip().lower() for e in admin_emails if e.strip()}

    async def execute(self, user_id: str, email: str) -> User:
        user = await self._users.find_by_id(user_id)
        if user is None:
            role = ROLE_ADMIN if email.lower() in self._admin_emails else ROLE_VIEWER
            user = User(
                id=user_id, email=email, role=role, active=True, created_at=datetime.now(UTC)
            )
            await self._users.save(user)
        return user


class ListUsersUseCase:
    def __init__(self, users: UsersRepository) -> None:
        self._users = users

    async def execute(self) -> list[User]:
        return await self._users.list_all()


class UpdateUserUseCase:
    def __init__(self, users: UsersRepository) -> None:
        self._users = users

    async def execute(
        self, actor_id: str, user_id: str, role: str | None = None, active: bool | None = None
    ) -> Either[Exception, User]:
        user = await self._users.find_by_id(user_id)
        if user is None:
            return Left(ResourceNotFoundError("User", user_id))
        if role is not None and role not in ALL_ROLES:
            return Left(NotAllowedError(f"unknown role {role}"))
        if user_id == actor_id and (
            (role is not None and role != ROLE_ADMIN) or active is False
        ):
            return Left(NotAllowedError("admin cannot demote or block themselves"))
        if role is not None:
            user.role = role
        if active is not None:
            user.active = active
        await self._users.save(user)
        return Right(user)
