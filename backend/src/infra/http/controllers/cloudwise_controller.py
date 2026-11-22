from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from domain.cloudwise.application.use_cases.get_dashboard import GetCostsUseCase, GetDashboardUseCase
from domain.cloudwise.enterprise.value_objects.cost_filters import CostFilters
from infra.database.repositories.sql_repositories import SQLCostsRepository
from infra.database.session import get_session
from infra.http.dtos.api_dtos import (
    CloudWiseDashboardDTO,
    CostRecordReadDTO,
    CostSeriesDayDTO,
    DashboardSummaryDTO,
)
from infra.http.middleware.easy_auth import AuthUser, get_current_user

router = APIRouter(prefix="/cloudwise", tags=["cloudwise"])


def cost_filters(
    service: str | None = None,
    start: date | None = None,
    end: date | None = None,
    subscription_id: str | None = None,
) -> CostFilters:
    return CostFilters(service=service, start=start, end=end, subscription_id=subscription_id)


@router.get("/costs", response_model=list[CostRecordReadDTO])
async def get_costs(
    session: Session = Depends(get_session),
    _user: AuthUser = Depends(get_current_user),
    filters: CostFilters = Depends(cost_filters),
) -> list[CostRecordReadDTO]:
    use_case = GetCostsUseCase(SQLCostsRepository(session))
    result = await use_case.execute(filters)
    if result.is_left():
        raise HTTPException(status_code=422, detail=str(result.value))
    records = result.value
    return [
        CostRecordReadDTO(
            id=str(r.id),
            subscription_id=r.subscription_id,
            cost=r.cost,
            date=r.record_date.isoformat(),
            resource_type=r.resource_type,
            tags=r.tags,
        )
        for r in records
    ]


@router.get("/dashboard", response_model=CloudWiseDashboardDTO)
async def get_dashboard(
    session: Session = Depends(get_session),
    _user: AuthUser = Depends(get_current_user),
    filters: CostFilters = Depends(cost_filters),
    granularity: str = "day",
) -> CloudWiseDashboardDTO:
    use_case = GetDashboardUseCase(SQLCostsRepository(session))
    outcome = await use_case.execute(filters, granularity)
    if outcome.is_left():
        raise HTTPException(status_code=422, detail=str(outcome.value))
    result = outcome.value
    return CloudWiseDashboardDTO(
        granularity=result.granularity,
        series=[
            CostSeriesDayDTO(
                date=s.date,
                total_cost=s.total_cost,
                by_service=s.by_service,
            )
            for s in result.series
        ],
        summary=DashboardSummaryDTO(
            total_cost=result.summary.total_cost,
            top_service=result.summary.top_service,
            subscription_count=result.summary.subscription_count,
        ),
    )
