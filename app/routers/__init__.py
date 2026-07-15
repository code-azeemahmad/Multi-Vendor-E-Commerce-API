from fastapi import FastAPI

from app.routers import auth, health, test


def register_routes(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(test.router)