# app/schemas/user.py

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import UserRole


class UserResponse(BaseModel):
    """
    Public representation of a user.
    """

    id: UUID
    email: str
    full_name: str
    phone: str | None
    profile_image_url: str |None

    role: UserRole

    is_verified: bool
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class UpdateProfileRequest(BaseModel):
    """
    Request model for updating the authenticated user's profile.
    """

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )