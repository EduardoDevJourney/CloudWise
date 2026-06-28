from dataclasses import dataclass

from domain.cloudwise.enterprise.entities.cost_dim import CostDim
from domain.cloudwise.enterprise.entities.cost_record import CostRecord


@dataclass(frozen=True, slots=True)
class DashboardSummary:
    total_cost: float
    top_service: str
    subscription_count: int


@dataclass(frozen=True, slots=True)
class CostSeriesDay:
    date: str
    total_cost: float
    by_service: dict[str, float]


@dataclass(frozen=True, slots=True)
class DashboardResult:
    granularity: str
    series: list[CostSeriesDay]
    summary: DashboardSummary


class GetCostsUseCase:
    def __init__(self, cost_repo: object) -> None:
        self._cost_repo = cost_repo

    async def execute(self) -> list[CostRecord]:
        return await self._cost_repo.list_all()


class GetDashboardUseCase:
    def __init__(self, cost_repo: object, dim_repo: object) -> None:
        self._cost_repo = cost_repo
        self._dim_repo = dim_repo

    async def execute(self) -> DashboardResult:
        records: list[CostRecord] = await self._cost_repo.list_all()
        dims: list[CostDim] = await self._dim_repo.list_all()

        by_date: dict[str, dict[str, float]] = {}
        subscription_ids: set[str] = set()
        service_totals: dict[str, float] = {}

        for record in records:
            date_key = record.record_date.isoformat()
            subscription_ids.add(record.subscription_id)
            by_date.setdefault(date_key, {})
            by_date[date_key][record.resource_type] = (
                by_date[date_key].get(record.resource_type, 0) + record.cost
            )
            service_totals[record.resource_type] = (
                service_totals.get(record.resource_type, 0) + record.cost
            )

        for dim in dims:
            service_totals[dim.service_name] = service_totals.get(dim.service_name, 0)

        series = [
            CostSeriesDay(
                date=date_key,
                total_cost=sum(services.values()),
                by_service=services,
            )
            for date_key, services in sorted(by_date.items())
        ]

        top_service = max(service_totals, key=service_totals.get, default="n/a")
        total_cost = sum(r.cost for r in records)

        return DashboardResult(
            granularity="day",
            series=series,
            summary=DashboardSummary(
                total_cost=total_cost,
                top_service=top_service,
                subscription_count=len(subscription_ids),
            ),
        )
