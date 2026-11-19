"""Política padrão da empresa para provisionamento.

Fonte única das regras de negócio. Python puro (sem importar pulumi), para que
o backend possa validar o pedido antes de executar e o Pulumi aplique as mesmas
regras ao criar os recursos.
"""

import re

ALLOWED_LOCATIONS = ("eastus", "eastus2", "brazilsouth")
ALLOWED_ENVIRONMENTS = ("dev", "hml", "prod")
REQUIRED_TAGS = ("project", "environment", "managed-by", "owner", "template")

# Nome lógico: minúsculas, números e hífen; 3 a 20 caracteres; começa com letra.
RESOURCE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,19}$")

STORAGE_SKU_BY_ENV = {"dev": "Standard_LRS", "hml": "Standard_LRS", "prod": "Standard_GRS"}


def validate_request(resource_name: str, environment: str, location: str) -> list[str]:
    """Devolve a lista de violações (vazia quando o pedido está conforme)."""
    violations: list[str] = []
    if not RESOURCE_NAME_PATTERN.match(resource_name or ""):
        violations.append(
            "resource_name deve ter 3 a 20 caracteres: minúsculas, números e hífen, começando por letra"
        )
    if environment not in ALLOWED_ENVIRONMENTS:
        violations.append(f"environment deve ser um de: {', '.join(ALLOWED_ENVIRONMENTS)}")
    if location not in ALLOWED_LOCATIONS:
        violations.append(f"location deve ser uma de: {', '.join(ALLOWED_LOCATIONS)}")
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


def storage_account_name(resource_name: str, environment: str) -> str:
    return f"sa{resource_name.replace('-', '')[:18]}{environment[:4]}"[:24]


def key_vault_name(resource_name: str, environment: str, suffix: str) -> str:
    """3-24 caracteres, único globalmente: o sufixo vem do id da solicitação."""
    return f"kv-{resource_name[:10]}-{environment[:4]}-{suffix[:4]}"[:24]


def storage_sku(environment: str) -> str:
    return STORAGE_SKU_BY_ENV[environment]


def key_vault_purge_protection(environment: str) -> bool:
    # Irreversível e reserva o nome do cofre: só em produção.
    return environment == "prod"
