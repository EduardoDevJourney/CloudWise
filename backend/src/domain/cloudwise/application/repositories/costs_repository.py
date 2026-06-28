from typing import Protocol

from domain.cloudwise.enterprise.entities.cost_dim import CostDim
from domain.cloudwise.enterprise.entities.cost_record import CostRecord


class CostRecordsRepository(Protocol):
    async def list_all(self) -> list[CostRecord]: ...

    async def save_many(self, records: list[CostRecord]) -> None: ...


class CostDimsRepository(Protocol):
    async def list_all(self) -> list[CostDim]: ...

    async def save_many(self, dims: list[CostDim]) -> None: ...
