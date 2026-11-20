from domain.runops.enterprise.entities.provision_request import ProvisionRequest
from domain.runops.enterprise.entities.template import Template


class InMemoryProvisionRequestsRepository:
    def __init__(self) -> None:
        self._items: dict[str, ProvisionRequest] = {}

    async def create(self, request: ProvisionRequest) -> None:
        self._items[str(request.id)] = request

    async def save(self, request: ProvisionRequest) -> None:
        self._items[str(request.id)] = request

    async def find_by_id(self, provision_id: str) -> ProvisionRequest | None:
        return self._items.get(provision_id)

    async def list_all(self) -> list[ProvisionRequest]:
        return list(self._items.values())


class InMemoryTemplatesRepository:
    def __init__(self) -> None:
        self._items: dict[str, Template] = {}

    async def find_by_id(self, template_id: str) -> Template | None:
        return self._items.get(template_id)

    async def list_all(self) -> list[Template]:
        return list(self._items.values())

    async def save(self, template: Template) -> None:
        self._items[template.slug] = template
