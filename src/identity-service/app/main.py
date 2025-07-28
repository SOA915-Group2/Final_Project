from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Table, Column, String, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import databases
import asyncio
import uuid
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from starlette.status import HTTP_401_UNAUTHORIZED
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from passlib.hash import bcrypt

# Database setup
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@identity-db:5432/identity_db"
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

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#def get_db():
#    db = SessionLocal()
#    try:
#        yield db
#    finally:
#        db.close()

# App init
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Allow requests from frontend (in Docker or local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:5173"] or ["http://frontend"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security settings
SECRET_KEY = "super-secret-key"  # Use environment variable in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting app")
    await database.connect()
    yield
    # Shutdown logic
    print("Shutting down app")
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Register user
@app.post("/register")
async def register(user: UserCreate):
    if await get_user(user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    user_id = str(uuid.uuid4())
    hashed = hash_password(user.password)
    query = users.insert().values(id=user_id, username=user.username, password_hash=hashed)
    await database.execute(query)
    return {"user_id": user_id}

@app.post("/login")
async def login(user: UserCreate):
    user_record = await get_user(user.username)
    if not user_record or not verify_password(user.password, user_record["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={
        "sub": user_record["id"],
        "username": user_record["username"]
    })
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route example
@app.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return {"user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.get("/users/validate")
async def validate_user(user_id: str):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"valid": True}

#@app.delete("/users/{username}", status_code=204)
#def delete_user(username: str, db: Session = Depends(get_db)):
#    user = db.query(users).filter(users.username == username).first()
#    if user:
#        db.delete(user)
#        db.commit()
#        return {"detail": "User deleted"}
#    else:
#        return {"detail": "User not found"}

# Serve React frontend build from ./static directory
static_path = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    app()
