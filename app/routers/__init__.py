from fastapi import FastAPI

from app.routers import auth, health, test, user


def register_routes(app: FastAPI) -> None:
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(test.router)
    app.include_router(user.router)