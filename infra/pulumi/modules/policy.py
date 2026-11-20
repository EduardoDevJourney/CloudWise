"""Company provisioning policy.

Single source of the business rules. Plain Python (no pulumi import) so the
backend can validate a request before running it and Pulumi applies the same
rules when creating the resources.
"""

import re

ALLOWED_LOCATIONS = ("eastus", "eastus2", "brazilsouth")
ALLOWED_ENVIRONMENTS = ("dev", "hml", "prod")

# Logical name: lowercase letters, digits and hyphens; 3 to 20 chars; starts with a letter.
RESOURCE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,19}$")

STORAGE_SKU_BY_ENV = {"dev": "Standard_LRS", "hml": "Standard_LRS", "prod": "Standard_GRS"}


def validate_request(resource_name: str, environment: str, location: str) -> list[str]:
    """Returns the list of violations (empty when the request complies)."""
    violations: list[str] = []
    if not RESOURCE_NAME_PATTERN.match(resource_name or ""):
        violations.append(
            "resource_name must be 3 to 20 characters: lowercase letters, digits and hyphens, "
            "starting with a letter"
        )
    if environment not in ALLOWED_ENVIRONMENTS:
        violations.append(f"environment must be one of: {', '.join(ALLOWED_ENVIRONMENTS)}")
    if location not in ALLOWED_LOCATIONS:
        violations.append(f"location must be one of: {', '.join(ALLOWED_LOCATIONS)}")
    return violations


def standard_tags(environment: str, owner: str, template: str) -> dict[str, str]:
    return {
        "project": "cloud-wise",
        "environment": environment,
        "managed-by": "pulumi",
        "owner": owner,
        "template": template,
    }


def resource_group_name(resource_name: str, environment: str) -> str:
    return f"rg-{resource_name}-{environment}"


def storage_account_name(resource_name: str, environment: str, suffix: str) -> str:
    """3-24 chars, lowercase letters and digits only, globally unique
    (suffix comes from the request id)."""
    compact = resource_name.replace("-", "")[:12]
    return f"sa{compact}{environment[:4]}{suffix.replace('-', '')[:6]}".lower()[:24]


def key_vault_name(resource_name: str, environment: str, suffix: str) -> str:
    """3-24 chars, globally unique (suffix comes from the request id)."""
    return f"kv-{resource_name[:10]}-{environment[:4]}-{suffix[:4]}"[:24]


def storage_sku(environment: str) -> str:
    return STORAGE_SKU_BY_ENV[environment]


def key_vault_purge_protection(environment: str) -> bool:
    # Irreversible and it reserves the vault name, so prod only.
    return environment == "prod"
