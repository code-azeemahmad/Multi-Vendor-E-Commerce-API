from __future__ import annotations


class AuthException(Exception):
    """
    Base exception for all authentication-related errors.
    """


class EmailAlreadyExistsError(AuthException):
    """
    Raised when attempting to register with an email that already exists.
    """


class InvalidCredentialsError(AuthException):
    """
    Raised when the provided email or password is invalid.
    """


class InvalidTokenError(AuthException):
    """
    Raised when a JWT is invalid.
    """


class ExpiredTokenError(AuthException):
    """
    Raised when a JWT has expired.
    """


class EmailNotVerifiedError(AuthException):
    """
    Raised when the user's email has not been verified.
    """


class InactiveUserError(AuthException):
    """
    Raised when a user account has been disabled.
    """
    

# app/exceptions/user.py


class UserException(Exception):
    """
    Base exception for user-related errors.
    """


class UserNotFoundError(UserException):
    """
    Raised when a user cannot be found.
    """
    

class AuthenticationRequiredError(AuthException):
    """
    Raised when authentication credentials are missing.
    """