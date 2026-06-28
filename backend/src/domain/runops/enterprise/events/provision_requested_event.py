from dataclasses import dataclass

from core.events.domain_event import DomainEvent


@dataclass(frozen=True, slots=True)
class ProvisionRequestedEvent(DomainEvent):
    provision_id: str
    user_id: str
    template_id: str


@dataclass(frozen=True, slots=True)
class ProvisionCompletedEvent(DomainEvent):
    provision_id: str
    user_id: str


@dataclass(frozen=True, slots=True)
class ProvisionFailedEvent(DomainEvent):
    provision_id: str
    user_id: str
    reason: str
