from collections import defaultdict
from collections.abc import Callable

from core.events.domain_event import DomainEvent

EventHandler = Callable[[DomainEvent], None]


class DomainEvents:
    _handlers: dict[type[DomainEvent], list[EventHandler]] = defaultdict(list)

    @classmethod
    def register(cls, event_type: type[DomainEvent], handler: EventHandler) -> None:
        cls._handlers[event_type].append(handler)

    @classmethod
    def dispatch(cls, event: DomainEvent) -> None:
        for handler in cls._handlers.get(type(event), []):
            handler(event)

    @classmethod
    def dispatch_events(cls, events: list[DomainEvent]) -> None:
        for event in events:
            cls.dispatch(event)
