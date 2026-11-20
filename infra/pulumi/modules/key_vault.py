import pulumi_azure_native as azure

from . import policy


def create(resource_name: str, environment: str, suffix: str, resource_group, tags: dict[str, str]):
    tenant_id = azure.authorization.get_client_config().tenant_id
    return azure.keyvault.Vault(
        "kv",
        vault_name=policy.key_vault_name(resource_name, environment, suffix),
        resource_group_name=resource_group.name,
        location=resource_group.location,
        properties=azure.keyvault.VaultPropertiesArgs(
            tenant_id=tenant_id,
            sku=azure.keyvault.SkuArgs(family="A", name="standard"),
            enable_rbac_authorization=True,
            enable_soft_delete=True,
            soft_delete_retention_in_days=7,
            # The API rejects an explicit False: either enable it or leave it out.
            enable_purge_protection=True if policy.key_vault_purge_protection(environment) else None,
        ),
        tags=tags,
    )
