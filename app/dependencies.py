from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import JWTService
from app.core.security import PasswordHasher
from app.database.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.services.auth import AuthService


@lru_cache
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


@lru_cache
def get_jwt_service() -> JWTService:
    return JWTService()


def get_auth_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    repository: Annotated[
        AuthRepository,
        Depends(get_auth_repository),
    ],
    password_hasher: Annotated[
        PasswordHasher,
        Depends(get_password_hasher),
    ],
    jwt_service: Annotated[
        JWTService,
        Depends(get_jwt_service),
    ],
) -> AuthService:
    return AuthService(
        repository=repository,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )
