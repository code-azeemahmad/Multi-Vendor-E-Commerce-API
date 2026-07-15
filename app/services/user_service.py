from __future__ import annotations

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
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
    ) -> None:
        self._repository = repository

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

        user = await self._repository.update(current_user)

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