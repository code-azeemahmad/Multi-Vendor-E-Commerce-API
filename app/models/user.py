from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import (
    ActiveMixin,
    Base,
    TimestampMixin,
    UUIDMixin,
)
from app.models.enums import UserRole


class User(
    Base,
    UUIDMixin,
    TimestampMixin,
    ActiveMixin,
):
    """
    User account model.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
    )

    profile_image_url: Mapped[str | None] = mapped_column(
        String(500),
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
        ),
        default=UserRole.CUSTOMER,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )