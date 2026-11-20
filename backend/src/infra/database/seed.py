import json
from datetime import date
from pathlib import Path

from sqlmodel import Session, select

from infra.database.sqlmodel.models import CostDimModel, CostRecordModel, TemplateModel


_PARAMS_SCHEMA = {
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


def seed_database(session: Session) -> None:
    existing_slugs = set(session.exec(select(TemplateModel.slug)).all())
    for template in TEMPLATES:
        if template["slug"] not in existing_slugs:
            session.add(TemplateModel(params_schema=json.dumps(_PARAMS_SCHEMA), **template))
        else:
            existing = session.exec(
                select(TemplateModel).where(TemplateModel.slug == template["slug"])
            ).first()
            if existing and not existing.description:
                existing.description = template["description"]
                session.add(existing)
    session.commit()

    if session.exec(select(CostRecordModel)).first():
        return

    raw = json.loads((Path(__file__).parent / "seed_data" / "costs.json").read_text())
    for i, item in enumerate(raw):
        session.add(
            CostRecordModel(
                id=item["id"],
                subscription_id=item["subscription_id"],
                cost=item["cost"],
                record_date=date.fromisoformat(item["date"]),
                resource_type=item["resource_type"],
                tags=json.dumps(item.get("tags", {})),
            )
        )
        session.add(
            CostDimModel(
                id=f"22222222-2222-4222-8222-2222222222{i:02d}",
                record_date=date.fromisoformat(item["date"]),
                category=item.get("category", "compute"),
                service_name=item["resource_type"],
            )
        )

    session.commit()
