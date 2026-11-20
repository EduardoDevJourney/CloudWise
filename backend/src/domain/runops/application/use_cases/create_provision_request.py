from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from core.either import Either, Left, Right
from core.events.domain_events import DomainEvents
from domain.runops.application.errors.not_allowed_error import NotAllowedError
from domain.runops.application.errors.policy_violation_error import PolicyViolationError
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError
from domain.runops.application.repositories.provision_requests_repository import (
    ProvisionRequestsRepository,
)
from domain.runops.application.repositories.templates_repository import TemplatesRepository
from domain.runops.enterprise.entities.provision_request import ProvisionRequest


@dataclass(frozen=True, slots=True)
class CreateProvisionRequestInput:
    user_id: str
    roles: list[str]
    template_id: str
    resource_name: str
    environment: str
    location: str


class CreateProvisionRequestUseCase:
    ALLOWED_ROLES = ("runops.provisioner", "runops.admin")

    def __init__(
        self,
        provision_repo: ProvisionRequestsRepository,
        templates_repo: TemplatesRepository,
        policy_validator: Callable[[str, str, str], list[str]] | None = None,
    ) -> None:
        self._provision_repo = provision_repo
        self._templates_repo = templates_repo
        self._policy_validator = policy_validator

    async def execute(
        self, input_data: CreateProvisionRequestInput
    ) -> Either[Exception, ProvisionRequest]:
        if not any(r in input_data.roles for r in self.ALLOWED_ROLES):
            return Left(NotAllowedError("provision resource"))

        template = await self._templates_repo.find_by_id(input_data.template_id)
        if template is None:
            return Left(ResourceNotFoundError("Template", input_data.template_id))

        if self._policy_validator is not None:
            violations = self._policy_validator(
                input_data.resource_name, input_data.environment, input_data.location
            )
            if violations:
                return Left(PolicyViolationError(violations))

        request_data: dict[str, Any] = {
            "template_id": input_data.template_id,
            "template": template.slug,
            "resource_name": input_data.resource_name,
            "environment": input_data.environment,
            "location": input_data.location,
        }

        request = ProvisionRequest.create(
            user_id=input_data.user_id,
            template_id=input_data.template_id,
            request_data=request_data,
        )

        await self._provision_repo.create(request)
        events = request.clear_domain_events()
        DomainEvents.dispatch_events(events)

        return Right(request)
