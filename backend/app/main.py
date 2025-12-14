import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import login
from app.core.config import settings
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    threading.Thread(target=init_db()).start()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    version=settings.version,
    prefix=settings.API_V1_STR,
)
app.include_router(login.router)
