from fastapi import FastAPI

from app.routers import auth, health


def register_routes(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(auth.router)