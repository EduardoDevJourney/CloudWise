from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from domain.auth.application.use_cases.manage_users import ListUsersUseCase, UpdateUserUseCase
from domain.runops.application.errors.not_allowed_error import NotAllowedError
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError
from infra.database.repositories.sql_repositories import SQLUsersRepository
from infra.database.session import get_session
from infra.http.dtos.api_dtos import MeDTO, UserReadDTO, UserUpdateDTO
from infra.http.middleware.easy_auth import ROLE_ADMIN, AuthUser, get_current_user, require_role

router = APIRouter(tags=["auth"])


def _to_dto(user) -> UserReadDTO:
    return UserReadDTO(
        id=user.id,
        email=user.email,
        role=user.role,
        active=user.active,
        created_at=user.created_at,
    )


@router.get("/me", response_model=MeDTO)
async def me(user: AuthUser = Depends(get_current_user)) -> MeDTO:
    return MeDTO(id=user.user_id, email=user.email, role=user.roles[0])


@router.get("/users", response_model=list[UserReadDTO])
async def list_users(
    session: Session = Depends(get_session),
    _admin: AuthUser = Depends(require_role(ROLE_ADMIN)),
) -> list[UserReadDTO]:
    users = await ListUsersUseCase(SQLUsersRepository(session)).execute()
    return [_to_dto(u) for u in users]


@router.patch("/users/{user_id}", response_model=UserReadDTO)
async def update_user(
    user_id: str,
    body: UserUpdateDTO,
    session: Session = Depends(get_session),
    admin: AuthUser = Depends(require_role(ROLE_ADMIN)),
) -> UserReadDTO:
    result = await UpdateUserUseCase(SQLUsersRepository(session)).execute(
        admin.user_id, user_id, role=body.role, active=body.active
    )
    if result.is_left():
        error = result.value
        if isinstance(error, ResourceNotFoundError):
            raise HTTPException(status_code=404, detail=str(error))
        if isinstance(error, NotAllowedError):
            raise HTTPException(status_code=400, detail=str(error))
        raise HTTPException(status_code=400, detail=str(error))
    return _to_dto(result.value)
