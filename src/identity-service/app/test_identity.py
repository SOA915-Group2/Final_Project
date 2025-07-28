import pytest
from httpx import AsyncClient
from .main import app, database
from fastapi.testclient import TestClient
from unittest.mock import patch

pytestmark = pytest.mark.asyncio

client = TestClient(app)

## Define a base URL
HOSTNAME = "34.44.171.179"
BASE_URL = f"http://{HOSTNAME}/api/identity"
@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(base_url=BASE_URL) as client:
        # Register a user
        register_resp = await client.post("/register", json={"username": "testuser2", "password": "secret"})
        assert register_resp.status_code == 200
        assert "user_id" in register_resp.json()

        # Login with the registered user
        login_resp = await client.post("/login", json={"username": "testuser2", "password": "secret"})
        assert login_resp.status_code == 200
        data = login_resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(base_url=BASE_URL) as client:
        resp = await client.post("/login", json={"username": "nouser", "password": "wrong"})
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Invalid credentials"

