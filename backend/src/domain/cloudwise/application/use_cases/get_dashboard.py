from dataclasses import dataclass

from core.either import Either, Left, Right
from domain.cloudwise.application.repositories.costs_repository import CostsRepository
from domain.cloudwise.enterprise.entities.cost_record import CostRecord
from domain.cloudwise.enterprise.value_objects.cost_aggregates import CostSummary
from domain.cloudwise.enterprise.value_objects.cost_filters import CostFilters, InvalidFilterError

GRANULARITIES = ("day", "month")


@dataclass(frozen=True, slots=True)
class CostSeriesDay:
    date: str
    total_cost: float
    by_service: dict[str, float]


@dataclass(frozen=True, slots=True)
class DashboardResult:
    granularity: str
    series: list[CostSeriesDay]
    summary: CostSummary


class GetCostsUseCase:
    def __init__(self, repository: CostsRepository) -> None:
        self._repository = repository

    async def execute(
        self, filters: CostFilters | None = None
    ) -> Either[InvalidFilterError, list[CostRecord]]:
        filters = filters or CostFilters()
        if (error := filters.validate()) is not None:
            return Left(error)
        return Right(await self._repository.list_records(filters))


class GetDashboardUseCase:
    def __init__(self, repository: CostsRepository) -> None:
        self._repository = repository

    async def execute(
        self, filters: CostFilters | None = None, granularity: str = "day"
    ) -> Either[InvalidFilterError, DashboardResult]:
        filters = filters or CostFilters()
        if (error := filters.validate()) is not None:
            return Left(error)
        if granularity not in GRANULARITIES:
            return Left(InvalidFilterError(f"granularity must be one of: {', '.join(GRANULARITIES)}"))

        by_period: dict[str, dict[str, float]] = {}
        for row in await self._repository.series(filters, granularity):
            by_period.setdefault(row.period, {})[row.service] = row.total

        series = [
            CostSeriesDay(date=period, total_cost=sum(services.values()), by_service=services)
            for period, services in sorted(by_period.items())
        ]
        summary = await self._repository.summary(filters)
        return Right(DashboardResult(granularity=granularity, series=series, summary=summary))
