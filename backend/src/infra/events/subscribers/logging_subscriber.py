import logging
from typing import Any

from core.events.domain_event import DomainEvent
from core.events.domain_events import DomainEvents
from domain.runops.enterprise.events.provision_completed_event import ProvisionCompletedEvent
from domain.runops.enterprise.events.provision_failed_event import ProvisionFailedEvent
from domain.runops.enterprise.events.provision_requested_event import ProvisionRequestedEvent

logger = logging.getLogger(__name__)


def _log_event(event: DomainEvent) -> None:
    logger.info("Domain event dispatched: %s", type(event).__name__)


def register_subscribers() -> None:
    DomainEvents.register(ProvisionRequestedEvent, _log_event)
    DomainEvents.register(ProvisionCompletedEvent, _log_event)
    DomainEvents.register(ProvisionFailedEvent, _log_event)
