import pytest
from httpx import AsyncClient
from .main import app, database
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)

@patch("app.database.connect")  # Mock the DB connect function
def test_root(mock_connect):
    mock_connect.return_value = None  # Prevent real DB connection
    response = client.get("/")
    assert response.status_code == 200

## Define a base URL
HOSTNAME = "34.44.171.179"
BASE_URL = f"http://{HOSTNAME}/api/identity"
@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://34.44.171.179/api/identity") as client:
        # Register a user
        register_resp = await client.post("/register", json={"username": "testuser", "password": "secret"})
        assert register_resp.status_code == 200
        assert "user_id" in register_resp.json()

        # Login with the registered user
        login_resp = await client.post("/login", json={"username": "testuser", "password": "secret"})
        assert login_resp.status_code == 200
        data = login_resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://34.44.171.179/api/identity") as client:
        resp = await client.post("/login", json={"username": "nouser", "password": "wrong"})
        assert resp.status_code == 401
        assert resp.json()["detail"] == "Invalid credentials"

