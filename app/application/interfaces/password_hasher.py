"""Protocol for password hashing operations."""

from typing import Protocol


class PasswordHasher(Protocol):
    """Interface for password hashing and verification."""

    def hash(self, password: str) -> str:
        """Hash a plain-text password.

        Args:
            password: The plain-text password.

        Returns:
            The hashed password string.
        """
        ...

    def verify(self, plain: str, hashed: str) -> bool:
        """Verify a plain-text password against a hash.

        Args:
            plain: The plain-text password to check.
            hashed: The previously hashed password.

        Returns:
            True if the password matches, False otherwise.
        """
        ...
