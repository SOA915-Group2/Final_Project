from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid, requests

app = FastAPI()

# In-memory "database"
orders = {}

class OrderRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int

@app.post("/api/orders")
def create_order(order: OrderRequest):
    # Validate user via identity-service
    try:
        response = requests.get("http://identity-service:8000/api/users/validate", params={"user_id": order.user_id})
        response.raise_for_status()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=401, detail="User validation failed")

    order_id = str(uuid.uuid4())
    orders[order_id] = {
        "user_id": order.user_id,
        "product_id": order.product_id,
        "quantity": order.quantity
    }
    return {"order_id": order_id}

@app.get("/api/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]
