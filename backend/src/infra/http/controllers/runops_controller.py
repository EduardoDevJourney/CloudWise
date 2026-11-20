import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session

from domain.runops.application.errors.not_allowed_error import NotAllowedError
from domain.runops.application.errors.policy_violation_error import PolicyViolationError
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError
from domain.runops.application.use_cases.create_provision_request import (
    CreateProvisionRequestInput,
    CreateProvisionRequestUseCase,
)
from domain.runops.application.use_cases.execute_provision import ExecuteProvisionUseCase
from domain.runops.application.use_cases.list_templates import ListTemplatesUseCase
from domain.runops.application.use_cases.get_provision_status import (
    GetProvisionStatusUseCase,
    ListProvisionRequestsUseCase,
)
from infra.database.repositories.sql_repositories import (
    SQLProvisionRequestsRepository,
    SQLTemplatesRepository,
)
from infra.database.session import engine, get_session
from infra.http.dtos.api_dtos import (
    PolicyReadDTO,
    ProvisionRequestCreateDTO,
    ProvisionRequestReadDTO,
    TemplateReadDTO,
)
from infra.http.middleware.easy_auth import (
    ROLE_ADMIN,
    ROLE_PROVISIONER,
    AuthUser,
    get_current_user,
    require_role,
)
from domain.runops.enterprise.value_objects.provision_status import ProvisionStatus
from infra.pulumi.policy_loader import load_policy
from infra.pulumi.pulumi_service import PulumiService

logger = logging.getLogger(__name__)
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
        started_at=request.started_at,
        finished_at=request.finished_at,
        execution_seconds=request.execution_seconds,
        outputs=request.outputs,
    )


async def _mark_failed(provision_id: str, reason: str) -> None:
    with Session(engine) as session:
        repo = SQLProvisionRequestsRepository(session)
        request = await repo.find_by_id(provision_id)
        if request is not None and request.status in (ProvisionStatus.PENDING, ProvisionStatus.RUNNING):
            request.fail(reason)
            await repo.save(request)


async def _run_provision(provision_id: str) -> None:
    # Tarefa em segundo plano: nenhuma exceção pode escapar nem deixar o pedido em RUNNING.
    try:
        with Session(engine) as session:
            provision_repo = SQLProvisionRequestsRepository(session)
            use_case = ExecuteProvisionUseCase(provision_repo, PulumiService())
            await use_case.execute(provision_id)
    except Exception as exc:
        logger.exception("Provision %s crashed", provision_id)
        try:
            await _mark_failed(provision_id, f"Internal error: {exc}")
        except Exception:
            logger.exception("Could not mark provision %s as FAILED", provision_id)


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
        policy_validator=load_policy().validate_request,
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
        if isinstance(error, PolicyViolationError):
            raise HTTPException(status_code=422, detail=error.violations)
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


@router.get("/templates", response_model=list[TemplateReadDTO])
async def list_templates(
    session: Session = Depends(get_session),
    _user: AuthUser = Depends(get_current_user),
) -> list[TemplateReadDTO]:
    templates = await ListTemplatesUseCase(SQLTemplatesRepository(session)).execute()
    return [
        TemplateReadDTO(
            id=str(t.id),
            slug=t.slug,
            name=t.name,
            description=t.description,
            params_schema=t.params_schema,
            azure_sku=t.azure_sku,
        )
        for t in templates
    ]


@router.get("/policy", response_model=PolicyReadDTO)
async def get_policy(_user: AuthUser = Depends(get_current_user)) -> PolicyReadDTO:
    policy = load_policy()
    return PolicyReadDTO(
        locations=list(policy.ALLOWED_LOCATIONS),
        environments=list(policy.ALLOWED_ENVIRONMENTS),
        resource_name_pattern=policy.RESOURCE_NAME_PATTERN.pattern,
    )
