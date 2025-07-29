# tests/e2e/test_user_flow.py
import pytest
import httpx

BASE_URL = "http://34.44.171.179"  # or your ingress LoadBalancer IP

@pytest.mark.asyncio
async def test_user_register_login_and_get_orders():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Register
        res = await client.post("/api/identity/register", json={
            "username": "e2euser2",
            "password": "e2epass"
        })
        assert res.status_code in [200, 201], f"Failed: {res.status_code} - {res.text}"

        # Login
        res = await client.post("/api/identity/login", json={
            "username": "e2euser",
            "password": "e2epass"
        })
        assert "access_token" in res.json()
        token = res.json()["access_token"]

        # Call product service
        headers = {"Authorization": f"Bearer {token}"}
        res = await client.get("/api/products", headers=headers)
        assert res.status_code == 200
