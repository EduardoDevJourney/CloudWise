from typing import Any, Protocol

from core.either import Either, Left, Right
from core.events.domain_events import DomainEvents
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError
from domain.runops.application.repositories.provision_requests_repository import (
    ProvisionRequestsRepository,
)
from domain.runops.enterprise.entities.provision_request import ProvisionRequest


class PulumiRunner(Protocol):
    async def up(self, stack_name: str, config: dict[str, Any]) -> None: ...


class ExecuteProvisionUseCase:
    def __init__(
        self,
        provision_repo: ProvisionRequestsRepository,
        pulumi_runner: PulumiRunner,
    ) -> None:
        self._provision_repo = provision_repo
        self._pulumi_runner = pulumi_runner

    async def execute(self, provision_id: str) -> Either[Exception, ProvisionRequest]:
        request = await self._provision_repo.find_by_id(provision_id)
        if request is None:
            return Left(ResourceNotFoundError("ProvisionRequest", provision_id))

        try:
            request.start()
            await self._provision_repo.save(request)

            await self._pulumi_runner.up(
                stack_name=f"provision-{provision_id}",
                config=request.request_data,
            )

            request.complete()
        except Exception as exc:
            request.fail(str(exc))

        await self._provision_repo.save(request)
        events = request.clear_domain_events()
        DomainEvents.dispatch_events(events)

        return Right(request)
