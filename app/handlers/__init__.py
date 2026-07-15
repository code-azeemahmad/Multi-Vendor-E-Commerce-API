from __future__ import annotations

from fastapi import FastAPI

from app.exceptions import (
    EmailAlreadyExistsError,
    EmailNotVerifiedError,
    ExpiredTokenError,
    InactiveUserError,
    InvalidCredentialsError,
    InvalidTokenError,
    PermissionDeniedError,
    PasswordReuseError,
    InvalidCurrentPasswordError,
)

from .auth import (
    email_already_exists_handler,
    email_not_verified_handler,
    expired_token_handler,
    inactive_user_handler,
    invalid_credentials_handler,
    invalid_token_handler,
    permission_denied_handler,
    password_reuse_handler,
    invalid_current_password_handler,   
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.
    """

    app.add_exception_handler(
        EmailAlreadyExistsError,
        email_already_exists_handler,
    )

    app.add_exception_handler(
        InvalidCredentialsError,
        invalid_credentials_handler,
    )

    app.add_exception_handler(
        InvalidTokenError,
        invalid_token_handler,
    )

    app.add_exception_handler(
        ExpiredTokenError,
        expired_token_handler,
    )

    app.add_exception_handler(
        EmailNotVerifiedError,
        email_not_verified_handler,
    )

    app.add_exception_handler(
        InactiveUserError,
        inactive_user_handler,
    )
    
    app.add_exception_handler(
        PermissionDeniedError,  
        permission_denied_handler
    )
    
    app.add_exception_handler(
        PasswordReuseError,
        password_reuse_handler
    )
    
    app.add_exception_handler(
        InvalidCurrentPasswordError,
        invalid_current_password_handler
    )