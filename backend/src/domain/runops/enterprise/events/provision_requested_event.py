from dataclasses import dataclass

from core.events.domain_event import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class ProvisionRequestedEvent(DomainEvent):
    provision_id: str
    user_id: str
    template_id: str
