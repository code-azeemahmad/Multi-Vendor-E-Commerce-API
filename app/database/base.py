from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    mapped_column,
)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """


@declarative_mixin
class UUIDMixin:
    """
    Provides a UUID primary key.
    """

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )


@declarative_mixin
class TimestampMixin:
    """
    Provides automatic created_at and updated_at timestamps.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


@declarative_mixin
class ActiveMixin:
    """
    Provides a reusable active/inactive flag.
    """

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )