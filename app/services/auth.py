from __future__ import annotations

from app.core.jwt import JWTService
from app.core.security import PasswordHasher
from app.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)


class AuthService:
    """
    Handles authentication business logic.
    """

    def __init__(
        self,
        repository: AuthRepository,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher
        self.jwt_service = jwt_service

    async def register(
        self,
        data: RegisterRequest,
    ) -> AuthResponse:
        """
        Register a new customer account.
        """
        existing_user = await self.repository.get_by_email(data.email)

        if existing_user:
            raise EmailAlreadyExistsError()

        hashed_password = self.password_hasher.hash(data.password)

        user = self._build_user(
            data=data,
            hashed_password=hashed_password,
        )

        user = await self.repository.create(user)

        return self._build_auth_response(user)

    async def login(
        self,
        data: LoginRequest,
    ) -> AuthResponse:
        """
        Authenticate a user and return JWT tokens.
        """
        user = await self.repository.get_by_email(data.email)

        if user is None:
            raise InvalidCredentialsError()

        if not self.password_hasher.verify(
            data.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError()

        return self._build_auth_response(user)

    def _build_user(
        self,
        *,
        data: RegisterRequest,
        hashed_password: str,
    ) -> User:
        """
        Construct a new User ORM instance.
        """
        return User(
            email=data.email,
            hashed_password=hashed_password,
            full_name=data.full_name,
            phone=data.phone,
            role=UserRole.CUSTOMER,
        )

    def _generate_tokens(
        self,
        user: User,
    ) -> TokenResponse:
        """
        Generate access and refresh tokens.
        """
        return TokenResponse(
            access_token=self.jwt_service.create_access_token(
                user_id=user.id,
                role=user.role,
            ),
            refresh_token=self.jwt_service.create_refresh_token(
                user_id=user.id,
                role=user.role,
            ),
        )

    def _build_auth_response(
        self,
        user: User,
    ) -> AuthResponse:
        """
        Build the authentication response.
        """
        return AuthResponse(
            user=UserResponse.model_validate(user),
            tokens=self._generate_tokens(user),
        )
        

'''
                 AuthService
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
AuthRepository   PasswordHasher   JWTService
      │
      ▼
 PostgreSQL

'''