# app/core/jwt.py
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt

from app.core.config import settings
from app.models.enums import TokenType, UserRole


class JWTService:
    """
    Service responsible for creating and decoding JWT tokens.
    """

    def create_access_token(
        self,
        *,
        user_id: UUID,
        role: UserRole,
    ) -> str:
        return self._create_token(
            user_id=user_id,
            role=role,
            token_type=TokenType.ACCESS,
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
        )

    def create_refresh_token(
        self,
        *,
        user_id: UUID,
        role: UserRole,
    ) -> str:
        return self._create_token(
            user_id=user_id,
            role=role,
            token_type=TokenType.REFRESH,
            expires_delta=timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ),
        )

    def decode_token(self, token: str) -> dict:
        """
        Decode and validate a JWT.

        Raises:
            jwt.ExpiredSignatureError
            jwt.InvalidTokenError
        """
        return jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    def _create_token(
        self,
        *,
        user_id: UUID,
        role: UserRole,
        token_type: TokenType,
        expires_delta: timedelta,
    ) -> str:
        payload = self._build_payload(
            user_id=user_id,
            role=role,
            token_type=token_type,
            expires_delta=expires_delta,
        )

        return jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def _build_payload(
        *,
        user_id: UUID,
        role: UserRole,
        token_type: TokenType,
        expires_delta: timedelta,
    ) -> dict:
        now = datetime.now(UTC)

        return {
            "sub": str(user_id),
            "role": role.value,
            "type": token_type.value,
            "jti": str(uuid4()),
            "iat": now,
            "exp": now + expires_delta,
        }