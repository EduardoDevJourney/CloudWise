import json
from datetime import date
from pathlib import Path

from sqlmodel import Session, select

from infra.database.sqlmodel.models import CostDimModel, CostRecordModel, TemplateModel


def seed_database(session: Session) -> None:
    existing = session.exec(select(TemplateModel)).first()
    if existing:
        return

    session.add(
        TemplateModel(
            id="00000000-0000-4000-8000-000000000001",
            name="Resource Group + Storage Account",
            params_schema=json.dumps(
                {
                    "type": "object",
                    "properties": {
                        "resource_name": {"type": "string"},
                        "environment": {"type": "string"},
                        "location": {"type": "string"},
                    },
                    "required": ["resource_name", "environment", "location"],
                }
            ),
            azure_sku="Standard_LRS",
            slug="rg-storage",
        )
    )

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
