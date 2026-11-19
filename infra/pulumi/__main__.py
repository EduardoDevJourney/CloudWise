import pulumi

from modules import key_vault, policy, resource_group, storage_account

config = pulumi.Config()
template = config.get("template") or "rg-storage"
resource_name = config.require("resource_name")
environment = config.require("environment")
location = config.get("location") or "eastus"
owner = config.get("owner") or "unknown"
request_id = config.get("request_id") or "0000"

violations = policy.validate_request(resource_name, environment, location)
if violations:
    raise Exception("Política violada: " + "; ".join(violations))

tags = policy.standard_tags(environment, owner, template)
rg = resource_group.create(resource_name, environment, location, tags)

if template == "rg-storage":
    sa = storage_account.create(resource_name, environment, rg, tags)
    pulumi.export("resource_group_name", rg.name)
    pulumi.export("storage_account_name", sa.name)
elif template == "rg-keyvault":
    kv = key_vault.create(resource_name, environment, request_id.replace("-", ""), rg, tags)
    pulumi.export("resource_group_name", rg.name)
    pulumi.export("key_vault_name", kv.name)
else:
    raise Exception(f"Template desconhecido: {template}")
