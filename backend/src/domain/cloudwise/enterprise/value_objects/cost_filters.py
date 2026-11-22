from dataclasses import dataclass
from datetime import date


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
