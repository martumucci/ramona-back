"""Password hashing using bcrypt directly."""

import bcrypt


class PasswordHasher:
    """Hashes and verifies passwords using bcrypt.

    Uses bcrypt.hashpw/checkpw directly instead of passlib,
    which has compatibility issues with bcrypt 4.x.
    """

    def hash(self, password: str) -> str:
        """Hash a plain-text password with bcrypt.

        Args:
            password: The plain-text password.

        Returns:
            The bcrypt-hashed password string.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, plain: str, hashed: str) -> bool:
        """Verify a plain-text password against a bcrypt hash.

        Args:
            plain: The plain-text password to check.
            hashed: The previously hashed password.

        Returns:
            True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(plain.encode(), hashed.encode())
