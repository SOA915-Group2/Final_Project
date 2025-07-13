from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Table, Column, String, MetaData, create_engine, select
import uuid
import databases

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/identity_db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("password", String),
)

engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
metadata.create_all(engine)

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/api/register")
async def register(user: UserIn):
    query = users.select().where(users.c.username == user.username)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = str(uuid.uuid4())
    query = users.insert().values(id=user_id, username=user.username, password=user.password)
    await database.execute(query)
    return {"user_id": user_id}

@app.get("/api/users/validate")
async def validate_user(user_id: str):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"valid": True}
