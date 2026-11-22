import json
import random
import uuid
from datetime import UTC, date, datetime, timedelta

from sqlmodel import Session, select

from domain.auth.roles import ROLE_ADMIN, ROLE_PROVISIONER, ROLE_VIEWER
from infra.database.sqlmodel.models import (
    DimAssinaturaModel,
    DimDataModel,
    DimServicoModel,
    FatoCustoModel,
    TemplateModel,
    UserModel,
)


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


DEV_USERS = [
    ("dev-viewer", "viewer@dev.local", ROLE_VIEWER),
    ("dev-provisioner", "provisioner@dev.local", ROLE_PROVISIONER),
    ("dev-user", "dev-user@dev.local", ROLE_ADMIN),
]


def seed_dev_users(session: Session) -> None:
    existing = set(session.exec(select(UserModel.id)).all())
    for user_id, email, role in DEV_USERS:
        if user_id not in existing:
            session.add(
                UserModel(
                    id=user_id,
                    email=email,
                    role=role,
                    active=True,
                    created_at=datetime.now(UTC),
                )
            )
    session.commit()


COST_START = date(2026, 6, 1)
COST_DAYS = 30
COST_SERVICES = [
    ("Microsoft.Storage", "storage", 40.0),
    ("Microsoft.Compute", "compute", 150.0),
    ("Microsoft.Network", "network", 25.0),
]
COST_SUBSCRIPTIONS = [
    ("sub-sandbox-001", "Sandbox 001", "dev", 1.0),
    ("sub-sandbox-002", "Sandbox 002", "prod", 0.6),
]
_COST_NAMESPACE = uuid.UUID("c0570000-0000-4000-8000-000000000000")


def seed_costs(session: Session) -> None:
    if session.exec(select(FatoCustoModel.id)).first():
        return

    rng = random.Random(42)
    days = [COST_START + timedelta(days=i) for i in range(COST_DAYS)]
    for day in days:
        session.add(
            DimDataModel(
                data_id=int(day.strftime("%Y%m%d")),
                data=day,
                ano=day.year,
                trimestre=(day.month - 1) // 3 + 1,
                mes=day.month,
                dia=day.day,
                dia_semana=day.weekday(),
                ano_mes=day.strftime("%Y-%m"),
            )
        )
    services = [DimServicoModel(nome=n, categoria=c) for n, c, _ in COST_SERVICES]
    subscriptions = [DimAssinaturaModel(codigo=c, nome=n) for c, n, _, _ in COST_SUBSCRIPTIONS]
    session.add_all(services + subscriptions)
    session.commit()

    for service, (name, _, base) in zip(services, COST_SERVICES):
        for subscription, (code, _, env, weight) in zip(subscriptions, COST_SUBSCRIPTIONS):
            for day in days:
                weekend = 0.7 if day.weekday() >= 5 else 1.0
                cost = round(base * weight * weekend * rng.uniform(0.8, 1.2), 2)
                session.add(
                    FatoCustoModel(
                        id=str(uuid.uuid5(_COST_NAMESPACE, f"{day}|{name}|{code}")),
                        data_id=int(day.strftime("%Y%m%d")),
                        servico_id=service.servico_id,
                        assinatura_id=subscription.assinatura_id,
                        custo=cost,
                        tags=json.dumps({"env": env}),
                    )
                )
    session.commit()


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

    seed_costs(session)
