import pytest
from httpx import AsyncClient

from infra.config import get_settings

BASE = "/api/v1"


@pytest.mark.asyncio
async def test_first_access_registers_user_as_viewer(client: AsyncClient):
    headers = {"X-Dev-User-Id": "newcomer", "X-Dev-User-Email": "newcomer@corp.com"}
    me = (await client.get(f"{BASE}/me", headers=headers)).json()
    assert me == {"id": "newcomer", "email": "newcomer@corp.com", "role": "runops.viewer"}


@pytest.mark.asyncio
async def test_admin_emails_bootstrap_first_admin(client: AsyncClient, monkeypatch):
    monkeypatch.setattr(get_settings(), "admin_emails", "boss@corp.com, other@corp.com")
    headers = {"X-Dev-User-Id": "boss", "X-Dev-User-Email": "Boss@corp.com"}
    assert (await client.get(f"{BASE}/me", headers=headers)).json()["role"] == "runops.admin"


@pytest.mark.asyncio
async def test_token_roles_are_ignored(client: AsyncClient, login):
    headers = {**login("viewer-x", "runops.viewer"), "X-Dev-User-Roles": "runops.admin"}
    assert (await client.get(f"{BASE}/users", headers=headers)).status_code == 403


@pytest.mark.asyncio
async def test_viewer_can_read_dashboard_but_not_manage_users(client: AsyncClient, login):
    headers = login("viewer-1", "runops.viewer")
    assert (await client.get(f"{BASE}/cloudwise/dashboard", headers=headers)).status_code == 200
    assert (await client.get(f"{BASE}/users", headers=headers)).status_code == 403


@pytest.mark.asyncio
async def test_admin_lists_and_changes_role(client: AsyncClient, login):
    admin = login("admin-u", "runops.admin")
    login("target-u", "runops.viewer")
    listed = (await client.get(f"{BASE}/users", headers=admin)).json()
    assert "target-u" in [u["id"] for u in listed]

    updated = await client.patch(f"{BASE}/users/target-u", json={"role": "runops.provisioner"}, headers=admin)
    assert updated.status_code == 200 and updated.json()["role"] == "runops.provisioner"
    assert (await client.patch(f"{BASE}/users/target-u", json={"role": "bogus"}, headers=admin)).status_code == 400
    assert (await client.patch(f"{BASE}/users/ghost", json={"active": False}, headers=admin)).status_code == 404


@pytest.mark.asyncio
async def test_blocked_user_gets_403(client: AsyncClient, login):
    admin = login("admin-b", "runops.admin")
    victim = login("victim-u", "runops.provisioner")
    assert (await client.get(f"{BASE}/me", headers=victim)).status_code == 200
    await client.patch(f"{BASE}/users/victim-u", json={"active": False}, headers=admin)
    assert (await client.get(f"{BASE}/me", headers=victim)).status_code == 403


@pytest.mark.asyncio
async def test_admin_cannot_demote_or_block_self(client: AsyncClient, login):
    admin = login("admin-self", "runops.admin")
    assert (await client.patch(f"{BASE}/users/admin-self", json={"role": "runops.viewer"}, headers=admin)).status_code == 400
    assert (await client.patch(f"{BASE}/users/admin-self", json={"active": False}, headers=admin)).status_code == 400
