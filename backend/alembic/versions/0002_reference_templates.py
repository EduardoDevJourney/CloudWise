"""reference data: template catalog

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-22
"""
import json
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PARAMS_SCHEMA = {
    "type": "object",
    "properties": {
        "resource_name": {"type": "string"},
        "environment": {"type": "string"},
        "location": {"type": "string"},
    },
    "required": ["resource_name", "environment", "location"],
}

TEMPLATES = [
    {
        "id": "00000000-0000-4000-8000-000000000001",
        "name": "Resource Group + Storage Account",
        "azure_sku": "Standard_LRS",
        "slug": "rg-storage",
        "description": (
            "Resource Group with a Storage Account "
            "(HTTPS only, TLS 1.2, no public access; SKU per environment)."
        ),
    },
    {
        "id": "00000000-0000-4000-8000-000000000002",
        "name": "Resource Group + Key Vault",
        "azure_sku": "standard",
        "slug": "rg-keyvault",
        "description": (
            "Resource Group with a Key Vault (RBAC, soft-delete; purge protection in prod only)."
        ),
    },
]

templates = sa.table(
    "templates",
    sa.column("id", sa.String),
    sa.column("name", sa.String),
    sa.column("params_schema", sa.Text),
    sa.column("azure_sku", sa.String),
    sa.column("slug", sa.String),
    sa.column("description", sa.Text),
)


def upgrade() -> None:
    op.bulk_insert(
        templates,
        [{**t, "params_schema": json.dumps(PARAMS_SCHEMA)} for t in TEMPLATES],
    )


def downgrade() -> None:
    slugs = [t["slug"] for t in TEMPLATES]
    op.execute(templates.delete().where(templates.c.slug.in_(slugs)))
