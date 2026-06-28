from dataclasses import dataclass, field
from datetime import date
from typing import Any

from core.entities.entity import Entity


@dataclass(eq=False, kw_only=True)
class CostRecord(Entity):
    subscription_id: str
    cost: float
    record_date: date
    resource_type: str
    tags: dict[str, Any] = field(default_factory=dict)
