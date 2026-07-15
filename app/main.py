from fastapi import FastAPI

from app.core.config import settings

from app.handlers.__init__ import register_exception_handlers
from app.routers.__init__ import register_routes

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

print(settings.DATABASE_URL)

register_exception_handlers(app)

register_routes(app)


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }