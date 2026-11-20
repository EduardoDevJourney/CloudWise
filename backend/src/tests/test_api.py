from httpx import AsyncClient


async def test_health(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_cloudwise_dashboard(client: AsyncClient, login):
    response = await client.get("/api/v1/cloudwise/dashboard", headers=login("t", "runops.viewer"))
    assert response.status_code == 200
    data = response.json()
    assert "series" in data
    assert "summary" in data
