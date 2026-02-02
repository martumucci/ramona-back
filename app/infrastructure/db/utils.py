"""Database utility helpers."""

from uuid import UUID

from app.domain.errors import ValidationError


def parse_uuid(value: str) -> UUID:
    """Parse a string as a UUID, raising a domain ValidationError on failure.

    Args:
        value: The string to parse.

    Returns:
        The parsed UUID.

    Raises:
        ValidationError: If the string is not a valid UUID.
    """
    try:
        return UUID(value)
    except ValueError as exc:
        raise ValidationError(f"Invalid UUID: {value}") from exc
