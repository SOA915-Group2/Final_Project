import pytest
from fastapi.testclient import TestClient
from main import app  # Ensure this points to your order-service FastAPI app

client = TestClient(app)

def test_create_order():
    order_data = {
        "user_id": "user123",
        "product_id": "product123",
        "quantity": 2
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["user_id"] == order_data["user_id"]
    assert data["product_id"] == order_data["product_id"]
    assert data["quantity"] == order_data["quantity"]
    assert "created_at" in data

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_order():
    # First, create a new order
    order_data = {
        "user_id": "user_single",
        "product_id": "product_single",
        "quantity": 1
    }
    create_response = client.post("/orders", json=order_data)
    assert create_response.status_code in [200, 201]
    order_id = create_response.json()["id"]

    # Then retrieve it
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_delete_order():
    # Create order first
    order_data = {
        "user_id": "user_delete",
        "product_id": "product_delete",
        "quantity": 1
    }
    create_response = client.post("/orders", json=order_data)
    assert create_response.status_code in [200, 201]
    order_id = create_response.json()["id"]

    # Delete it
    delete_response = client.delete(f"/orders/{order_id}")
    assert delete_response.status_code in [200, 204]

    # Try fetching again
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404
