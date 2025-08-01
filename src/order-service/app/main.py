from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
import uuid
from datetime import datetime

from fastapi import Header

def get_current_user(authorization: str = Header(...)):
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload.get("sub")

def serialize_order(order):
    return {
        "id": str(order["_id"]),
        "product_name": order.get("product_name", "N/A"),
        "quantity": order.get("quantity", 1),
        "created_at": order.get("created_at", "")
    }

app = FastAPI()

# Security settings
SECRET_KEY = "super-secret-key"  # Use environment variable in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# MongoDB setup
MONGO_DETAILS = "mongodb://mongodb:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.order_db
orders_collection = db.orders
products_collection = db["products"]

# Allow requests from frontend (in Docker or local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:5173"] or ["http://frontend"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OrderRequest(BaseModel):
    product_id: str
    quantity: int

class OrderResponse(BaseModel):
    _id: str
    product_id: str
    quantity: int
    user_id: str
    created_at: datetime

@app.post("/", response_model=OrderResponse)
async def place_order(order: OrderRequest, user_id: str = Depends(get_current_user)):
    print("Received order request:", order)
    new_order = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "placed",
        "created_at": datetime.utcnow(),
    }
    result = await orders_collection.insert_one(new_order)
    print("Incoming order:", order.dict())
    return {
      "_id": str(result.inserted_id),
      "product_id": order.product_id,
      "quantity": order.quantity,
      "user_id": user_id,
      "created_at": new_order["created_at"]
    }

@app.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["_id"] = str(order["_id"])
    return order

@app.get("/")
async def get_orders(user_id: str = Depends(get_current_user)):
    cursor = orders_collection.find({"user_id": user_id})
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return results
