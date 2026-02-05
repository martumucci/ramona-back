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

    def __init__(self, *, secret: str, expire_minutes: int, refresh_expire_days: int = 7) -> None:
        self._secret = secret
        self._expire_minutes = expire_minutes
        self._refresh_expire_days = refresh_expire_days

    def generate(self, user_id: str) -> str:
        """Generate a signed JWT for the given user.

        Args:
            user_id: The user's unique identifier to embed in the token.

        Returns:
            A signed JWT string.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {"sub": user_id, "exp": expire, "type": "access"}
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def generate_refresh_token(self, user_id: str) -> str:
        """Generate a signed refresh token (longer lived)"""
        expire = datetime.now(timezone.utc) + timedelta(days=self._refresh_expire_days)
        payload = {"sub": user_id, "exp": expire, "type": "refresh"}
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def verify(self, token: str, expected_type: str = "access") -> str:
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
            token_type: str | None = payload.get("type")

            if user_id is None:
                raise AuthenticationError("Invalid token")
            if token_type != expected_type:
                raise AuthenticationError("Invalid token type")
            return user_id
        except jwt.PyJWTError as exc:
            raise AuthenticationError("Invalid token") from exc
