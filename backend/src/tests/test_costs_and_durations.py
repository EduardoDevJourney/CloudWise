from datetime import UTC, datetime, timedelta

from httpx import AsyncClient

from domain.runops.enterprise.entities.provision_request import ProvisionRequest

BASE = "/api/v1"


async def test_costs_filter_by_service_and_subscription(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    everything = (await client.get(f"{BASE}/cloudwise/costs", headers=h)).json()
    assert everything
    service = everything[0]["resource_type"]
    by_service = (await client.get(f"{BASE}/cloudwise/costs", params={"service": service}, headers=h)).json()
    assert by_service and {r["resource_type"] for r in by_service} == {service}
    sub = everything[0]["subscription_id"]
    by_sub = (await client.get(f"{BASE}/cloudwise/costs", params={"subscription_id": sub}, headers=h)).json()
    assert {r["subscription_id"] for r in by_sub} == {sub}


async def test_costs_filter_by_period_and_invalid_range(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    one_day = (await client.get(f"{BASE}/cloudwise/costs", params={"start": "2026-06-01", "end": "2026-06-01"}, headers=h)).json()
    assert one_day and {r["date"] for r in one_day} == {"2026-06-01"}
    bad = await client.get(f"{BASE}/cloudwise/costs", params={"start": "2026-06-05", "end": "2026-06-01"}, headers=h)
    assert bad.status_code == 422
    bad_dash = await client.get(f"{BASE}/cloudwise/dashboard", params={"start": "2026-06-05", "end": "2026-06-01"}, headers=h)
    assert bad_dash.status_code == 422


async def test_dashboard_summary_respects_filters(client: AsyncClient, login):
    h = login("cost-viewer", "runops.viewer")
    full = (await client.get(f"{BASE}/cloudwise/dashboard", headers=h)).json()
    day = (await client.get(f"{BASE}/cloudwise/dashboard", params={"start": "2026-06-01", "end": "2026-06-01"}, headers=h)).json()
    assert day["summary"]["total_cost"] < full["summary"]["total_cost"]
    assert [s["date"] for s in day["series"]] == ["2026-06-01"]


def test_execution_seconds_is_finish_minus_start():
    request = ProvisionRequest.create("u", "rg-storage", {})
    assert request.execution_seconds is None
    request.start()
    request.finished_at = request.started_at + timedelta(seconds=42.04)
    assert request.execution_seconds == 42.0


async def test_status_exposes_duration_after_run(client: AsyncClient, login, monkeypatch):
    class Runner:
        async def up(self, stack_name, config):
            return None

    monkeypatch.setattr("infra.http.controllers.runops_controller.PulumiService", Runner)
    h = login("dur-user", "runops.provisioner")
    payload = {"template_id": "rg-storage", "resource_name": "duration", "environment": "dev", "location": "eastus"}
    created = (await client.post(f"{BASE}/runops/provision", json=payload, headers=h)).json()
    body = (await client.get(f"{BASE}/runops/status/{created['id']}", headers=h)).json()
    assert body["started_at"] and body["finished_at"]
    assert body["execution_seconds"] is not None and body["execution_seconds"] >= 0


async def test_templates_expose_description_and_params(client: AsyncClient, login):
    h = login("tpl-user", "runops.viewer")
    templates = (await client.get(f"{BASE}/runops/templates", headers=h)).json()
    assert templates
    for t in templates:
        assert t["description"]
        assert "resource_name" in t["params_schema"]["properties"]
