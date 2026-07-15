from __future__ import annotations

from app.core.security import PasswordHasher
from app.exceptions.auth import InvalidCurrentPasswordError, PasswordReuseError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    ChangePasswordRequest,
    UpdateProfileRequest,
    UserResponse,
)


class UserService:
    """
    Business logic for user management.
    """

    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self.repository = repository
        self.password_hasher = password_hasher

    async def update_profile(
        self,
        current_user: User,
        data: UpdateProfileRequest,
    ) -> UserResponse:
        """
        Update the authenticated user's profile.
        """

        update_data = data.model_dump(
            exclude_unset=True,
        )

        if not update_data:
            return UserResponse.model_validate(current_user)

        self._apply_updates(
            current_user,
            update_data,
        )

        user = await self.repository.update(current_user)

        return UserResponse.model_validate(user)

    @staticmethod
    def _apply_updates(
        user: User,
        updates: dict[str, object],
    ) -> None:
        """
        Apply partial updates to a user instance.
        """

        for field, value in updates.items():
            setattr(user, field, value)

    async def change_password(
        self,
        current_user: User,
        data: ChangePasswordRequest,
    ) -> None:
        """
        Change the authenticated user's password.
        """

        if not self.password_hasher.verify(
            data.current_password,
            current_user.hashed_password,
        ):
            raise InvalidCurrentPasswordError()

        if self.password_hasher.verify(
            data.new_password,
            current_user.hashed_password,
        ):
            raise PasswordReuseError()

        current_user.hashed_password = self.password_hasher.hash(
            data.new_password,
        )

        await self.repository.update(current_user)
