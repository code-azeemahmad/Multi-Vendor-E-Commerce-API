from functools import lru_cache

from app.core.security import PasswordHasher


@lru_cache
def get_password_hasher() -> PasswordHasher:
    """
    Returns the shared PasswordHasher instance.
    """
    return PasswordHasher()