from domain.cloudwise.enterprise.entities.cost_dim import CostDim
from domain.cloudwise.enterprise.entities.cost_record import CostRecord


class InMemoryCostRecordsRepository:
    def __init__(self) -> None:
        self._items: list[CostRecord] = []

    async def list_all(self) -> list[CostRecord]:
        return list(self._items)

    async def save_many(self, records: list[CostRecord]) -> None:
        self._items.extend(records)


class InMemoryCostDimsRepository:
    def __init__(self) -> None:
        self._items: list[CostDim] = []

    async def list_all(self) -> list[CostDim]:
        return list(self._items)

    async def save_many(self, dims: list[CostDim]) -> None:
        self._items.extend(dims)
