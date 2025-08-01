import pytest
from fastapi.testclient import TestClient
from main import app  # adjust if your FastAPI app is in another file

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_product():
    new_product = {
        "name": "Test Product",
        "price": 19.99,
        "stock": 50
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["name"] == new_product["name"]
    assert "id" in data

def test_get_single_product():
    # First create product
    new_product = {
        "name": "Single Product",
        "price": 9.99,
        "stock": 20
    }
    create_response = client.post("/products", json=new_product)
    assert create_response.status_code in [200, 201]
    created_product = create_response.json()
    product_id = created_product["id"]

    # Then get the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Single Product"

def test_delete_product():
    # Create product first
    new_product = {
        "name": "Delete Product",
        "price": 5.99,
        "stock": 10
    }
    create_response = client.post("/products", json=new_product)
    product_id = create_response.json()["id"]

    # Delete product
    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code in [200, 204]

    # Ensure it's deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
