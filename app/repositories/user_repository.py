from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """
    Handles user-related database operations.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Retrieve a user by ID.
        """
        statement = (
            select(User)
            .where(User.id == user_id)
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    async def update(
        self,
        user: User,
    ) -> User:
        """
        Persist changes to an existing user.
        """

        await self._db.flush()
        await self._db.refresh(user)

        return user