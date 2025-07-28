import pytest
from httpx import AsyncClient
from .main import app

## Define a base URL
# HOSTNAME = "34.44.171.179"
DENTITY_API = "http://identity-service.default.svc.cluster.local:8000/api/identity"
PRODUCT_API = "http://product-service.default.svc.cluster.local:8000/api/products"

@pytest.mark.asyncio
async def test_register_login_and_get_products():
    test_user = {
        "username": "integration_user",
        "password": "testpass123"
    }

    async with httpx.AsyncClient() as client:
        # 1. Register
        reg_response = await client.post(f"{IDENTITY_API}/register", json=test_user)
        assert reg_response.status_code in (200, 201)

        # 2. Login
        login_payload = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        login_response = await client.post(f"{IDENTITY_API}/login", json=login_payload)
        assert login_response.status_code == 200
        token = login_response.json().get("access_token")
        assert token is not None

        # 3. Get products (authorized)
        headers = {"Authorization": f"Bearer {token}"}
        prod_response = await client.get(f"{PRODUCT_API}/", headers=headers)
        assert prod_response.status_code == 200
        assert isinstance(prod_response.json(), list)
