from core.entities.unique_entity_id import UniqueEntityId
from domain.runops.application.use_cases.create_provision_request import (
    CreateProvisionRequestInput,
    CreateProvisionRequestUseCase,
)
from domain.runops.enterprise.entities.template import Template
from tests.repositories.in_memory_runops_repositories import (
    InMemoryProvisionRequestsRepository,
    InMemoryTemplatesRepository,
)


async def test_create_provision_request_success():
    provision_repo = InMemoryProvisionRequestsRepository()
    templates_repo = InMemoryTemplatesRepository()
    template = Template(
        id=UniqueEntityId(),
        name="RG + Storage",
        params_schema={},
        azure_sku="Standard_LRS",
        slug="rg-storage",
    )
    await templates_repo.save(template)

    use_case = CreateProvisionRequestUseCase(provision_repo, templates_repo)
    result = await use_case.execute(
        CreateProvisionRequestInput(
            user_id="user-1",
            roles=["runops.provisioner"],
            template_id="rg-storage",
            resource_name="myapp",
            environment="dev",
            location="eastus",
        )
    )

    assert result.is_right()
    assert result.value.status.value == "pending"


async def test_create_provision_request_forbidden_without_role():
    provision_repo = InMemoryProvisionRequestsRepository()
    templates_repo = InMemoryTemplatesRepository()
    use_case = CreateProvisionRequestUseCase(provision_repo, templates_repo)

    result = await use_case.execute(
        CreateProvisionRequestInput(
            user_id="user-1",
            roles=[],
            template_id="rg-storage",
            resource_name="myapp",
            environment="dev",
            location="eastus",
        )
    )

    assert result.is_left()
