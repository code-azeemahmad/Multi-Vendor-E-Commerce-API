from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.dependencies import get_auth_service, get_current_user, get_user_service
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.schemas.user import ChangePasswordRequest
from app.services.auth import AuthService
from app.services.user_service import UserService

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


@router.post(
    "/refresh",
    response_model=AuthResponse,
    summary="Refresh JWT tokens",
)
async def refresh(
    data: RefreshTokenRequest,
    service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> AuthResponse:
    return await service.refresh_tokens(
        data.refresh_token,
    )


@router.patch(
    "/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change password",
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    service: Annotated[
        UserService,
        Depends(get_user_service),
    ],
) -> Response:
    await service.change_password(
        current_user=current_user,
        data=data,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )