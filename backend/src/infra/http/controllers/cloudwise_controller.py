from fastapi import APIRouter, Depends
from sqlmodel import Session

from domain.cloudwise.application.use_cases.get_dashboard import GetCostsUseCase, GetDashboardUseCase
from infra.database.repositories.sql_repositories import SQLCostDimsRepository, SQLCostRecordsRepository
from infra.database.session import get_session
from infra.http.dtos.api_dtos import (
    CloudWiseDashboardDTO,
    CostRecordReadDTO,
    CostSeriesDayDTO,
    DashboardSummaryDTO,
)

router = APIRouter(prefix="/cloudwise", tags=["cloudwise"])


@router.get("/costs", response_model=list[CostRecordReadDTO])
async def get_costs(session: Session = Depends(get_session)) -> list[CostRecordReadDTO]:
    use_case = GetCostsUseCase(SQLCostRecordsRepository(session))
    records = await use_case.execute()
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
async def get_dashboard(session: Session = Depends(get_session)) -> CloudWiseDashboardDTO:
    use_case = GetDashboardUseCase(
        SQLCostRecordsRepository(session),
        SQLCostDimsRepository(session),
    )
    result = await use_case.execute()
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
