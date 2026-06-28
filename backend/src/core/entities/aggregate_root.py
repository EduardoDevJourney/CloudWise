from dataclasses import dataclass, field

from core.entities.entity import Entity
from core.events.domain_event import DomainEvent


@dataclass(eq=False)
class AggregateRoot(Entity):
    _domain_events: list[DomainEvent] = field(default_factory=list, repr=False)

    def add_domain_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def clear_domain_events(self) -> list[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events
