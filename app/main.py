from fastapi import FastAPI
from app.routers import health

from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(health.router)

@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }