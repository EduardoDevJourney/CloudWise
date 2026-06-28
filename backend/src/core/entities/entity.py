from abc import ABC
from dataclasses import dataclass, field

from core.entities.unique_entity_id import UniqueEntityId


@dataclass(eq=False)
class Entity(ABC):
    id: UniqueEntityId = field(default_factory=UniqueEntityId)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
