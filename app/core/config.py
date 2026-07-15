from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    APP_NAME: str
    APP_VERSION: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    DEBUG: bool = False

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()