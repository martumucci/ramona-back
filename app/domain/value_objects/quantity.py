"""Quantity value object ensuring non-negative integer amounts."""

from dataclasses import dataclass

from app.domain.errors import ValidationError


@dataclass(frozen=True)
class Quantity:
    """Represents a countable quantity.

    Args:
        value: The quantity. Must be non-negative.

    Raises:
        ValidationError: If value is negative.
    """

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValidationError("Quantity cannot be negative")
