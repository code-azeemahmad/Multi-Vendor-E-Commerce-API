from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import jwt
from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError as PyJWTInvalidTokenError,
)

from app.core.config import settings
from app.exceptions import ExpiredTokenError, InvalidTokenError
from app.models.enums import TokenType, UserRole
from app.schemas.token import TokenPayload


class JWTService:
    """
    Service responsible for creating, validating,
    and decoding JWT tokens.
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

    def decode_token(
        self,
        token: str,
    ) -> TokenPayload:
        """
        Decode and validate a JWT.

        Raises:
            ExpiredTokenError
            InvalidTokenError
        """
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            return TokenPayload.model_validate(payload)

        except ExpiredSignatureError as exc:
            raise ExpiredTokenError() from exc

        except (
            InvalidSignatureError,
            DecodeError,
            PyJWTInvalidTokenError,
        ) as exc:
            raise InvalidTokenError() from exc

    def verify_access_token(
        self,
        token: str,
    ) -> TokenPayload:
        """
        Verify that the token is a valid access token.
        """
        payload = self.decode_token(token)

        if payload.type != TokenType.ACCESS:
            raise InvalidTokenError()

        return payload

    def verify_refresh_token(
        self,
        token: str,
    ) -> TokenPayload:
        """
        Verify that the token is a valid refresh token.
        """
        payload = self.decode_token(token)

        if payload.type != TokenType.REFRESH:
            raise InvalidTokenError()

        return payload

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
    ) -> dict[str, any]:
        now = datetime.now(UTC)

        return {
            "sub": str(user_id),
            "role": role.value,
            "type": token_type.value,
            "jti": str(uuid4()),
            "iat": now,
            "exp": now + expires_delta,
        }