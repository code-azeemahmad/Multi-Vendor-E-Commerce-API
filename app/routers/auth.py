from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_auth_service, get_current_user
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
    UserResponse,
)
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> AuthResponse:
    """
    Register a new customer account.
    """
    return await service.register(data)


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> AuthResponse:
    """
    Authenticate a user and return JWT tokens.
    """
    return await service.login(data)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current authenticated user",
)
async def me(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
) -> UserResponse:
    """
    Return the currently authenticated user.
    """

    return UserResponse.model_validate(current_user)