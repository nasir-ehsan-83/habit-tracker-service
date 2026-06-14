from fastapi import FastAPI
from contextlib import asynccontextmanager
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

# add routes from app/routes/
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(habit.router)
