import pulumi_azure_native as azure

from . import policy


def create(resource_name: str, environment: str, location: str, tags: dict[str, str]):
    return azure.resources.ResourceGroup(
        "rg",
        resource_group_name=policy.resource_group_name(resource_name, environment),
        location=location,
        tags=tags,
    )
