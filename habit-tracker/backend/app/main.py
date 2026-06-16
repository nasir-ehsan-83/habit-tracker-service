from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from fastapi_offline_docs.offline_docs import setup_offline_docs

from app.db.database import init_db
from app.routes import (
    auth, 
    habit, 
    user
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db() 
    yield

app = FastAPI(
    docs_url = False, 
    redoc_url = False, 
    lifespan = lifespan
)

setup_offline_docs(app)

# add cores middleware
app.add_middleware(
    CORSMiddleware,
    alowed_origins = [
        "http://localhost:3000",    # for react dev
        "http://127.0.0.1:5500",    # for liveserver
        "https://www.google.com"    # for google
    ],
    alowed_credintials = True,
    alowed_methods = ["GET, POST, DELETE, PATCH", "PUT"],
    alowed_headers = ["*"]
)

# add routes from app/routes/
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(habit.router)
