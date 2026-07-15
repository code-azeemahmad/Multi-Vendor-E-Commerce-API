from __future__ import annotations

from datetime import datetime # noqa
from uuid import UUID

from pydantic import BaseModel

from app.models.enums import UserRole, TokenType


class TokenPayload(BaseModel):
    sub: UUID
    role: UserRole
    type: TokenType

    jti: UUID

    iat: datetime
    exp: datetime