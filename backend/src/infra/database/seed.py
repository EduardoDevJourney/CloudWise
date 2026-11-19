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
    },
    {
        "id": "00000000-0000-4000-8000-000000000002",
        "name": "Resource Group + Key Vault",
        "azure_sku": "standard",
        "slug": "rg-keyvault",
    },
]


def seed_database(session: Session) -> None:
    existing_slugs = set(session.exec(select(TemplateModel.slug)).all())
    for template in TEMPLATES:
        if template["slug"] not in existing_slugs:
            session.add(TemplateModel(params_schema=json.dumps(_PARAMS_SCHEMA), **template))
    session.commit()

    if session.exec(select(CostRecordModel)).first():
        return

    seed_path = Path(__file__).parent / "seed_data" / "costs.json"
    if seed_path.exists():
        raw = json.loads(seed_path.read_text())
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
