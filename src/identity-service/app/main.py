from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import Table, Column, String, MetaData, create_engine
import databases
import uuid
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette.status import HTTP_401_UNAUTHORIZED

# Database setup
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/identity_db"
database = databases.Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("username", String, unique=True, index=True),
    Column("password_hash", String),
)

engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
metadata.create_all(engine)

# App init
app = FastAPI()

# Security settings
SECRET_KEY = "super-secret-key"  # Use environment variable in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Schemas
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def hash_password(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    query = users.select().where(users.c.username == username)
    return await database.fetch_one(query)

# FastAPI startup
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Register user
@app.post("/api/register")
async def register(user: UserCreate):
    if await get_user(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    user_id = str(uuid.uuid4())
    hashed = hash_password(user.password)
    query = users.insert().values(id=user_id, username=user.username, password_hash=hashed)
    await database.execute(query)
    return {"user_id": user_id}

# Login and get token
@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route example
@app.get("/api/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
