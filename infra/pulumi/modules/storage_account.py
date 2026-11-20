import pulumi_azure_native as azure

from . import policy


def create(resource_name: str, environment: str, suffix: str, resource_group, tags: dict[str, str]):
    return azure.storage.StorageAccount(
        "sa",
        account_name=policy.storage_account_name(resource_name, environment, suffix),
        resource_group_name=resource_group.name,
        location=resource_group.location,
        sku=azure.storage.SkuArgs(name=policy.storage_sku(environment)),
        kind="StorageV2",
        enable_https_traffic_only=True,
        minimum_tls_version="TLS1_2",
        allow_blob_public_access=False,
        tags=tags,
    )
