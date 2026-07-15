from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import JWTService
from app.core.security import PasswordHasher
from app.database.database import get_db
from app.exceptions.auth import AuthenticationRequiredError, InactiveUserError, UserNotFoundError
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.services.auth import AuthService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(
    auto_error=False,
)

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


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security),
    ],
    repository: Annotated[
        AuthRepository,
        Depends(get_auth_repository),
    ],
    jwt_service: Annotated[
        JWTService,
        Depends(get_jwt_service),
    ],
) -> User:
    """
    Authenticate the current request and return the current user.
    """

    if credentials is None:
        raise AuthenticationRequiredError()

    token = credentials.credentials

    payload = jwt_service.verify_access_token(token)

    user = await repository.get_by_id(payload.sub)

    if user is None:
        raise UserNotFoundError()

    if not user.is_active:
        raise InactiveUserError()

    return user