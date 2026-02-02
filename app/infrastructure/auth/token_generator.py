"""JWT token generation and verification using PyJWT."""

from datetime import datetime, timedelta, timezone

import jwt

from app.domain.errors import AuthenticationError

_ALGORITHM = "HS256"


class TokenGenerator:
    """Generates and verifies JWT access tokens.

    Args:
        secret: The signing secret key.
        expire_minutes: Token lifetime in minutes.
    """

    def __init__(self, *, secret: str, expire_minutes: int) -> None:
        self._secret = secret
        self._expire_minutes = expire_minutes

    def generate(self, user_id: str) -> str:
        """Generate a signed JWT for the given user.

        Args:
            user_id: The user's unique identifier to embed in the token.

        Returns:
            A signed JWT string.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {"sub": user_id, "exp": expire}
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def verify(self, token: str) -> str:
        """Verify a JWT and extract the user ID.

        Args:
            token: The JWT string to verify.

        Returns:
            The user ID from the token payload.

        Raises:
            AuthenticationError: If the token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self._secret, algorithms=[_ALGORITHM])
            user_id: str | None = payload.get("sub")
            if user_id is None:
                raise AuthenticationError("Invalid token")
            return user_id
        except jwt.PyJWTError as exc:
            raise AuthenticationError("Invalid token") from exc
