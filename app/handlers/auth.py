from __future__ import annotations

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    EmailAlreadyExistsError,
    EmailNotVerifiedError,
    ExpiredTokenError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
)


async def email_already_exists_handler(
    request: Request,
    exc: EmailAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Email is already registered.",
        },
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid email or password.",
        },
    )


async def invalid_token_handler(
    request: Request,
    exc: InvalidTokenError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid authentication token.",
        },
    )


async def expired_token_handler(
    request: Request,
    exc: ExpiredTokenError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Authentication token has expired.",
        },
    )


async def email_not_verified_handler(
    request: Request,
    exc: EmailNotVerifiedError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "Email address has not been verified.",
        },
    )


async def inactive_user_handler(
    request: Request,
    exc: InactiveUserError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "User account is inactive.",
        },
    )