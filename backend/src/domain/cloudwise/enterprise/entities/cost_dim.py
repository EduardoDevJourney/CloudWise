from dataclasses import dataclass
from datetime import date

from core.entities.entity import Entity


@dataclass(eq=False, kw_only=True)
class CostDim(Entity):
    record_date: date
    category: str
    service_name: str
