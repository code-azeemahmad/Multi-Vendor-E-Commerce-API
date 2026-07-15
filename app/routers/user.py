from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_user_service,
)
from app.models.user import User
from app.schemas.user import (
    UpdateProfileRequest,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current authenticated user",
)
async def get_me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_me(
    data: UpdateProfileRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> UserResponse:
    return await service.update_profile(
        current_user=current_user,
        data=data,
    )