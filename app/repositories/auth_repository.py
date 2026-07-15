# app/repositories/auth_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class AuthRepository:

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        result = await self._db.execute(statement)

        return result.scalar_one_or_none()

    async def create(
        self,
        user: User,
    ) -> User:

        self._db.add(user)

        await self._db.flush()

        await self._db.refresh(user)

        return user