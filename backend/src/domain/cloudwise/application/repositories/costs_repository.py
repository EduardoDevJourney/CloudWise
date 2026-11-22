from typing import Protocol

from domain.cloudwise.enterprise.entities.cost_record import CostRecord
from domain.cloudwise.enterprise.value_objects.cost_aggregates import CostSeriesRow, CostSummary
from domain.cloudwise.enterprise.value_objects.cost_filters import CostFilters


class CostsRepository(Protocol):
    async def list_records(self, filters: CostFilters) -> list[CostRecord]: ...

    async def series(self, filters: CostFilters, granularity: str) -> list[CostSeriesRow]: ...

    async def summary(self, filters: CostFilters) -> CostSummary: ...
