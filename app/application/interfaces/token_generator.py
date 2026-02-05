"""Protocol for JWT token operations."""

from typing import Protocol


class TokenGenerator(Protocol):
    """Interface for generating and verifying authentication tokens."""

    def generate(self, user_id: str) -> str:
        """Generate a new access token for the given user.

        Args:
            user_id: The user's unique identifier.

        Returns:
            A signed JWT token string.
        """
        ...

    def generate_refresh_token(self, user_id: str) -> str:
        """Generate a new refresh token"""
        ...

    def verify(self, token: str, expected_type: str = "access") -> str:
        """Verify a token and extract the user ID.

        Args:
            token: The JWT token to verify.

        Returns:
            The user ID embedded in the token.

        Raises:
            AuthenticationError: If the token is invalid or expired.
        """
        ...
