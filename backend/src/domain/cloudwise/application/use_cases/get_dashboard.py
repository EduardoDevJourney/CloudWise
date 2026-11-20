from dataclasses import dataclass
from datetime import date

from core.either import Either, Left, Right

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


class InvalidFilterError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class CostFilters:
    service: str | None = None
    start: date | None = None
    end: date | None = None
    subscription_id: str | None = None

    def validate(self) -> InvalidFilterError | None:
        if self.start and self.end and self.start > self.end:
            return InvalidFilterError("start must be before or equal to end")
        return None

    def matches(self, record: CostRecord) -> bool:
        return (
            (self.service is None or record.resource_type == self.service)
            and (self.subscription_id is None or record.subscription_id == self.subscription_id)
            and (self.start is None or record.record_date >= self.start)
            and (self.end is None or record.record_date <= self.end)
        )


class GetCostsUseCase:
    def __init__(self, cost_repo: object) -> None:
        self._cost_repo = cost_repo

    async def execute(
        self, filters: CostFilters | None = None
    ) -> Either[InvalidFilterError, list[CostRecord]]:
        filters = filters or CostFilters()
        if (error := filters.validate()) is not None:
            return Left(error)
        records = await self._cost_repo.list_all()
        return Right([r for r in records if filters.matches(r)])


class GetDashboardUseCase:
    def __init__(self, cost_repo: object, dim_repo: object) -> None:
        self._cost_repo = cost_repo
        self._dim_repo = dim_repo

    async def execute(
        self, filters: CostFilters | None = None
    ) -> Either[InvalidFilterError, DashboardResult]:
        filters = filters or CostFilters()
        if (error := filters.validate()) is not None:
            return Left(error)
        records: list[CostRecord] = [
            r for r in await self._cost_repo.list_all() if filters.matches(r)
        ]
        dims: list[CostDim] = [
            d
            for d in await self._dim_repo.list_all()
            if filters.service is None or d.service_name == filters.service
        ]

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

        return Right(
            DashboardResult(
                granularity="day",
                series=series,
                summary=DashboardSummary(
                    total_cost=total_cost,
                    top_service=top_service,
                    subscription_count=len(subscription_ids),
                ),
            )
        )
