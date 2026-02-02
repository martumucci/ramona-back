"""Data transfer objects for the application layer."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthResult:
    """Result of a successful authentication operation.

    Attributes:
        access_token: The JWT access token.
        token_type: The token type (always "bearer").
        user_id: The authenticated user's ID.
        name: The authenticated user's display name.
    """

    access_token: str
    token_type: str
    user_id: str
    name: str
