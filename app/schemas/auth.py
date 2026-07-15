from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field



from app.schemas.user import UserResponse


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )
    full_name: str = Field(
        min_length=2,
        max_length=255,
    )
    phone: str | None = Field(
        default=None,
        max_length=30,
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
    
    
class RefreshTokenRequest(BaseModel):
    """
    Request body for refreshing JWT tokens.
    """

    refresh_token: str