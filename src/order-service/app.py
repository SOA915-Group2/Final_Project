from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import motor.motor_asyncio

app = FastAPI()

# MongoDB setup
MONGO_DETAILS = "mongodb://db:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
db = client.order_db
order_collection = db.get_collection("orders")

class OrderRequest(BaseModel):
    user_id: str
    product_id: str
    quantity: int

class OrderResponse(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    product_id: str
    quantity: int

@app.post("/api/orders", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    order_doc = order.dict()
    result = await order_collection.insert_one(order_doc)
    order_doc["_id"] = str(result.inserted_id)
    return order_doc

@app.get("/api/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    order = await order_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["_id"] = str(order["_id"])
    return order
