from httpx import AsyncClient
from sqlalchemy import func
from sqlmodel import Session, select

from infra.database.seed import COST_DAYS, COST_SERVICES, COST_SUBSCRIPTIONS, seed_costs
from infra.database.session import engine
from infra.database.sqlmodel.models import (
    DimAssinaturaModel,
    DimDataModel,
    DimServicoModel,
    FatoCustoModel,
)

BASE = "/api/v1/cloudwise"


def _count(session: Session, model) -> int:
    return session.exec(select(func.count()).select_from(model)).one()


def test_seed_fills_dimensions_and_facts(app):
    with Session(engine) as session:
        assert _count(session, DimDataModel) == COST_DAYS
        assert _count(session, DimServicoModel) == len(COST_SERVICES)
        assert _count(session, DimAssinaturaModel) == len(COST_SUBSCRIPTIONS)
        assert _count(session, FatoCustoModel) == COST_DAYS * len(COST_SERVICES) * len(
            COST_SUBSCRIPTIONS
        )


def test_every_fact_joins_the_three_dimensions(app):
    with Session(engine) as session:
        joined = session.exec(
            select(func.count())
            .select_from(FatoCustoModel)
            .join(DimDataModel, FatoCustoModel.data_id == DimDataModel.data_id)
            .join(DimServicoModel, FatoCustoModel.servico_id == DimServicoModel.servico_id)
            .join(
                DimAssinaturaModel,
                FatoCustoModel.assinatura_id == DimAssinaturaModel.assinatura_id,
            )
        ).one()
        assert joined == _count(session, FatoCustoModel)


def test_seed_is_idempotent(app):
    with Session(engine) as session:
        before = _count(session, FatoCustoModel)
        seed_costs(session)
        assert _count(session, FatoCustoModel) == before


async def test_daily_series_matches_the_facts(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    dashboard = (await client.get(f"{BASE}/dashboard", headers=h)).json()
    with Session(engine) as session:
        total = session.exec(select(func.sum(FatoCustoModel.custo))).one()

    assert len(dashboard["series"]) == COST_DAYS
    assert round(sum(day["total_cost"] for day in dashboard["series"]), 2) == round(total, 2)
    assert round(dashboard["summary"]["total_cost"], 2) == round(total, 2)
    assert dashboard["summary"]["subscription_count"] == len(COST_SUBSCRIPTIONS)


async def test_monthly_granularity_adds_up_the_days(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    daily = (await client.get(f"{BASE}/dashboard", headers=h)).json()
    monthly = (await client.get(f"{BASE}/dashboard", params={"granularity": "month"}, headers=h)).json()

    assert monthly["granularity"] == "month"
    assert [s["date"] for s in monthly["series"]] == ["2026-06"]
    assert round(monthly["series"][0]["total_cost"], 2) == round(
        sum(day["total_cost"] for day in daily["series"]), 2
    )


async def test_invalid_granularity_is_rejected(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    response = await client.get(f"{BASE}/dashboard", params={"granularity": "year"}, headers=h)
    assert response.status_code == 422


async def test_subscription_count_follows_the_filters(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    one_sub = (
        await client.get(
            f"{BASE}/dashboard", params={"subscription_id": COST_SUBSCRIPTIONS[0][0]}, headers=h
        )
    ).json()

    assert one_sub["summary"]["subscription_count"] == 1
    assert one_sub["summary"]["top_service"] == "Microsoft.Compute"
