from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
import databases
import asyncio
from jose import jwt, JWTError
from typing import List
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

from fastapi import Header

def get_current_user(authorization: str = Header(...)):
    scheme, token = authorization.split()
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload.get("sub")

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@product-db:5432/product_db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

from sqlalchemy import update as sql_update, delete as sql_delete

# Define table
products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("price", Float),
    Column("description", String),
    Column("owner_id", String),
)

# Create engine
engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
metadata.create_all(engine)

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

# Schemas
class ProductIn(BaseModel):
    name: str
    price: float
    description: str

class ProductOut(ProductIn):
    id: int
    owner_id: str

# Auth util
#def get_current_user(token: str):
#    try:
#        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#        return payload["sub"]
#    except JWTError:
#        raise HTTPException(status_code=401, detail="Invalid token")

# Startup/shutdown
@app.on_event("startup")
async def startup():
    for _ in range(10):
        try:
            await database.connect()
            break
        except Exception:
            await asyncio.sleep(2)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Routes
@app.get("/", response_model=List[ProductOut])
async def list_products():
    query = products.select()
    return await database.fetch_all(query)

@app.post("/", response_model=ProductOut)
async def create_product(product: ProductIn, token: str = Depends(get_current_user)):
    query = products.insert().values(**product.dict(), owner_id=token)
    product_id = await database.execute(query)
    return {**product.dict(), "id": product_id, "owner_id": token}

@app.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductIn, token: str = Depends(get_current_user)):
    query = sql_update(products).where(products.c.id == product_id).values(
        name=product.name,
        price=product.price,
        description=product.description
    )
    await database.execute(query)
    return {**product.dict(), "id": product_id, "owner_id": token}

@app.delete("/{product_id}")
async def delete_product(product_id: int, token: str = Depends(get_current_user)):
    query = sql_delete(products).where(products.c.id == product_id)
    await database.execute(query)
    return {"deleted": True}
