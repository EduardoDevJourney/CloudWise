from typing import Protocol

from domain.runops.enterprise.entities.template import Template


class TemplatesRepository(Protocol):
    async def find_by_id(self, template_id: str) -> Template | None: ...

    async def list_all(self) -> list[Template]: ...

    async def save(self, template: Template) -> None: ...
