from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UniqueEntityId:
    value: UUID

    def __init__(self, value: UUID | str | None = None) -> None:
        if value is None:
            object.__setattr__(self, "value", uuid4())
        elif isinstance(value, str):
            object.__setattr__(self, "value", UUID(value))
        else:
            object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UniqueEntityId):
            return False
        return self.value == other.value
