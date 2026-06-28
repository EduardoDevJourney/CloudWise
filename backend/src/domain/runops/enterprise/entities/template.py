from dataclasses import dataclass, field
from typing import Any

from core.entities.entity import Entity
from core.entities.unique_entity_id import UniqueEntityId


@dataclass(eq=False)
class Template(Entity):
    name: str
    params_schema: dict[str, Any]
    azure_sku: str
    slug: str = ""

    def __post_init__(self) -> None:
        if not self.slug:
            self.slug = str(self.id)
