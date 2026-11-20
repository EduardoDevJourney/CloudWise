from domain.runops.application.repositories.templates_repository import TemplatesRepository
from domain.runops.enterprise.entities.template import Template


class ListTemplatesUseCase:
    def __init__(self, templates_repo: TemplatesRepository) -> None:
        self._templates_repo = templates_repo

    async def execute(self) -> list[Template]:
        return await self._templates_repo.list_all()
