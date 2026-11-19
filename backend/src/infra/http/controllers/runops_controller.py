from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session

from domain.runops.application.errors.not_allowed_error import NotAllowedError
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError
from domain.runops.application.use_cases.create_provision_request import (
    CreateProvisionRequestInput,
    CreateProvisionRequestUseCase,
)
from domain.runops.application.use_cases.execute_provision import ExecuteProvisionUseCase
from domain.runops.application.use_cases.get_provision_status import (
    GetProvisionStatusUseCase,
    ListProvisionRequestsUseCase,
)
from infra.database.repositories.sql_repositories import (
    SQLProvisionRequestsRepository,
    SQLTemplatesRepository,
)
from infra.database.session import engine, get_session
from infra.http.dtos.api_dtos import ProvisionRequestCreateDTO, ProvisionRequestReadDTO
from infra.http.middleware.easy_auth import (
    ROLE_ADMIN,
    ROLE_PROVISIONER,
    AuthUser,
    get_current_user,
    require_role,
)
from infra.pulumi.pulumi_service import PulumiService

router = APIRouter(prefix="/runops", tags=["runops"])


def _to_read_dto(request) -> ProvisionRequestReadDTO:
    return ProvisionRequestReadDTO(
        id=str(request.id),
        user_id=request.user_id,
        template_id=request.template_id,
        status=request.status.value,
        request_data=request.request_data,
        error_message=request.error_message,
        created_at=request.created_at,
        execution_time=request.execution_time,
    )


async def _run_provision(provision_id: str) -> None:
    with Session(engine) as session:
        provision_repo = SQLProvisionRequestsRepository(session)
        use_case = ExecuteProvisionUseCase(provision_repo, PulumiService())
        await use_case.execute(provision_id)


@router.post("/provision", response_model=ProvisionRequestReadDTO, status_code=202)
async def create_provision(
    body: ProvisionRequestCreateDTO,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    user: AuthUser = Depends(require_role(ROLE_PROVISIONER, ROLE_ADMIN)),
) -> ProvisionRequestReadDTO:
    use_case = CreateProvisionRequestUseCase(
        SQLProvisionRequestsRepository(session),
        SQLTemplatesRepository(session),
    )
    result = await use_case.execute(
        CreateProvisionRequestInput(
            user_id=user.user_id,
            roles=user.roles,
            template_id=body.template_id,
            resource_name=body.resource_name,
            environment=body.environment,
            location=body.location,
        )
    )

    if result.is_left():
        error = result.value
        if isinstance(error, NotAllowedError):
            raise HTTPException(status_code=403, detail=str(error))
        if isinstance(error, ResourceNotFoundError):
            raise HTTPException(status_code=404, detail=str(error))
        raise HTTPException(status_code=400, detail=str(error))

    provision = result.value
    background_tasks.add_task(_run_provision, str(provision.id))
    return _to_read_dto(provision)


@router.get("/status/{provision_id}", response_model=ProvisionRequestReadDTO)
async def get_status(
    provision_id: str,
    session: Session = Depends(get_session),
    user: AuthUser = Depends(get_current_user),
) -> ProvisionRequestReadDTO:
    use_case = GetProvisionStatusUseCase(SQLProvisionRequestsRepository(session))
    result = await use_case.execute(
        provision_id, user_id=user.user_id, is_admin=ROLE_ADMIN in user.roles
    )
    if result.is_left():
        raise HTTPException(status_code=404, detail=str(result.value))
    return _to_read_dto(result.value)


@router.get("/requests", response_model=list[ProvisionRequestReadDTO])
async def list_requests(
    session: Session = Depends(get_session),
    user: AuthUser = Depends(get_current_user),
) -> list[ProvisionRequestReadDTO]:
    use_case = ListProvisionRequestsUseCase(SQLProvisionRequestsRepository(session))
    requests = await use_case.execute(user_id=user.user_id, is_admin=ROLE_ADMIN in user.roles)
    return [_to_read_dto(r) for r in requests]
