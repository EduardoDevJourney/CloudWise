import pulumi
import pulumi_azure_native as azure

config = pulumi.Config()
resource_name = config.require("resource_name")
environment = config.require("environment")
location = config.get("location") or "eastus"

tags = {
    "project": "cloud-wise",
    "environment": environment,
    "managed-by": "pulumi",
}

resource_group = azure.resources.ResourceGroup(
    "rg",
    resource_group_name=f"rg-{resource_name}-{environment}",
    location=location,
    tags=tags,
)

storage_account = azure.storage.StorageAccount(
    "sa",
    account_name=f"sa{resource_name.replace('-', '')[:18]}{environment[:4]}",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    sku=azure.storage.SkuArgs(name=azure.storage.StorageAccountSkuName.STANDARD_LRS),
    kind=azure.storage.Kind.STORAGE_V2,
    tags=tags,
)

pulumi.export("resource_group_name", resource_group.name)
pulumi.export("storage_account_name", storage_account.name)
