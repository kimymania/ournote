from fastapi import FastAPI

from app.api.routes import login

app = FastAPI(prefix="/api/v1")
app.include_router(login.router)
