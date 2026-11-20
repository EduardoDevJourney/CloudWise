from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from core.entities.aggregate_root import AggregateRoot
from core.entities.unique_entity_id import UniqueEntityId
from domain.runops.enterprise.events.provision_completed_event import (
    ProvisionCompletedEvent,
)
from domain.runops.enterprise.events.provision_failed_event import ProvisionFailedEvent
from domain.runops.enterprise.events.provision_requested_event import (
    ProvisionRequestedEvent,
)
from domain.runops.enterprise.value_objects.provision_status import ProvisionStatus


@dataclass(eq=False, kw_only=True)
class ProvisionRequest(AggregateRoot):
    user_id: str
    template_id: str
    status: ProvisionStatus = ProvisionStatus.PENDING
    request_data: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    started_at: datetime | None = None
    finished_at: datetime | None = None

    @classmethod
    def create(
        cls,
        user_id: str,
        template_id: str,
        request_data: dict[str, Any],
        entity_id: UniqueEntityId | None = None,
    ) -> "ProvisionRequest":
        request = cls(
            id=entity_id or UniqueEntityId(),
            user_id=user_id,
            template_id=template_id,
            request_data=request_data,
        )
        request.add_domain_event(
            ProvisionRequestedEvent(
                provision_id=str(request.id),
                user_id=user_id,
                template_id=template_id,
            )
        )
        return request

    @property
    def execution_seconds(self) -> float | None:
        if self.started_at is None or self.finished_at is None:
            return None
        start = self.started_at.replace(tzinfo=None)
        end = self.finished_at.replace(tzinfo=None)
        return round((end - start).total_seconds(), 1)

    def start(self) -> None:
        if self.status != ProvisionStatus.PENDING:
            raise ValueError("Only pending requests can be started")
        self.status = ProvisionStatus.RUNNING
        self.started_at = datetime.now(UTC)

    def complete(self) -> None:
        if self.status != ProvisionStatus.RUNNING:
            raise ValueError("Only running requests can be completed")
        self.status = ProvisionStatus.SUCCESS
        self.finished_at = datetime.now(UTC)
        self.add_domain_event(
            ProvisionCompletedEvent(provision_id=str(self.id), user_id=self.user_id)
        )

    def fail(self, reason: str) -> None:
        if self.status not in (ProvisionStatus.PENDING, ProvisionStatus.RUNNING):
            raise ValueError("Cannot fail a terminal request")
        self.status = ProvisionStatus.FAILED
        self.error_message = reason
        self.finished_at = datetime.now(UTC)
        self.add_domain_event(
            ProvisionFailedEvent(
                provision_id=str(self.id),
                user_id=self.user_id,
                reason=reason,
            )
        )
