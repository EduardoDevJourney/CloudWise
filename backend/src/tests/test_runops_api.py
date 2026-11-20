import pytest
from httpx import AsyncClient

from infra.config import get_settings

PAYLOAD = {
    "template_id": "rg-storage",
    "resource_name": "rbac-test",
    "environment": "dev",
    "location": "eastus",
}


@pytest.fixture(autouse=True)
def no_real_provisioning(monkeypatch):
    async def _noop(_provision_id: str) -> None:
        return None

    monkeypatch.setattr("infra.http.controllers.runops_controller._run_provision", _noop)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path",
    ["/api/v1/runops/requests", "/api/v1/runops/status/x", "/api/v1/cloudwise/dashboard", "/api/v1/cloudwise/costs"],
)
async def test_requests_without_identity_return_401(client: AsyncClient, path: str):
    assert (await client.get(path)).status_code == 401


@pytest.mark.asyncio
async def test_create_without_identity_returns_401(client: AsyncClient):
    assert (await client.post("/api/v1/runops/provision", json=PAYLOAD)).status_code == 401


@pytest.mark.asyncio
async def test_dev_headers_ignored_outside_development(client: AsyncClient, monkeypatch):
    monkeypatch.setattr(get_settings(), "app_env", "production")
    response = await client.get("/api/v1/runops/requests", headers={"X-Dev-User-Id": "u1"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_viewer_gets_403_on_create(client: AsyncClient, login):
    response = await client.post("/api/v1/runops/provision", json=PAYLOAD, headers=login("u1", "runops.viewer"))
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_provisioner_sees_only_own_requests_and_admin_sees_all(client: AsyncClient, login):
    created = await client.post("/api/v1/runops/provision", json=PAYLOAD, headers=login("owner-1", "runops.provisioner"))
    assert created.status_code == 202
    provision_id = created.json()["id"]

    own = await client.get("/api/v1/runops/requests", headers=login("owner-1", "runops.provisioner"))
    assert provision_id in [r["id"] for r in own.json()]

    other = await client.get("/api/v1/runops/requests", headers=login("owner-2", "runops.provisioner"))
    assert provision_id not in [r["id"] for r in other.json()]

    hidden = await client.get(f"/api/v1/runops/status/{provision_id}", headers=login("owner-2", "runops.provisioner"))
    assert hidden.status_code == 404

    admin = await client.get("/api/v1/runops/requests", headers=login("admin-1", "runops.admin"))
    assert provision_id in [r["id"] for r in admin.json()]
    shown = await client.get(f"/api/v1/runops/status/{provision_id}", headers=login("admin-1", "runops.admin"))
    assert shown.status_code == 200


@pytest.mark.asyncio
async def test_policy_violation_returns_422_and_creates_nothing(client: AsyncClient, login):
    bad = {**PAYLOAD, "location": "westeurope", "environment": "qa"}
    headers = login("policy-user", "runops.provisioner")
    response = await client.post("/api/v1/runops/provision", json=bad, headers=headers)
    assert response.status_code == 422
    assert len(response.json()["detail"]) == 2
    listed = await client.get("/api/v1/runops/requests", headers=headers)
    assert listed.json() == []


@pytest.mark.asyncio
async def test_templates_catalog_and_policy_endpoints(client: AsyncClient, login):
    headers = login("u1", "runops.provisioner")
    templates = (await client.get("/api/v1/runops/templates", headers=headers)).json()
    assert {t["slug"] for t in templates} >= {"rg-storage", "rg-keyvault"}
    policy = (await client.get("/api/v1/runops/policy", headers=headers)).json()
    assert "eastus" in policy["locations"] and "dev" in policy["environments"]
