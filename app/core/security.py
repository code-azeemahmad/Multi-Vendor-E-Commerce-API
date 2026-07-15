from pwdlib import PasswordHash


class PasswordHasher:
    """
    Handles password hashing and verification using Argon2.
    """

    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        """
        Hash a plain-text password.
        """
        return self._password_hash.hash(password)

    def verify(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain-text password against its hash.
        """
        return self._password_hash.verify(
            plain_password,
            hashed_password,
        )