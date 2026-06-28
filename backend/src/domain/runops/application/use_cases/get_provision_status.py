from core.either import Either, Left, Right
from domain.runops.application.errors.resource_not_found_error import ResourceNotFoundError
from domain.runops.application.repositories.provision_requests_repository import (
    ProvisionRequestsRepository,
)
from domain.runops.enterprise.entities.provision_request import ProvisionRequest


class GetProvisionStatusUseCase:
    def __init__(self, provision_repo: ProvisionRequestsRepository) -> None:
        self._provision_repo = provision_repo

    async def execute(self, provision_id: str) -> Either[Exception, ProvisionRequest]:
        request = await self._provision_repo.find_by_id(provision_id)
        if request is None:
            return Left(ResourceNotFoundError("ProvisionRequest", provision_id))
        return Right(request)


class ListProvisionRequestsUseCase:
    def __init__(self, provision_repo: ProvisionRequestsRepository) -> None:
        self._provision_repo = provision_repo

    async def execute(self) -> list[ProvisionRequest]:
        return await self._provision_repo.list_all()
