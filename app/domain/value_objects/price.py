"""Price value object ensuring non-negative monetary amounts."""

from dataclasses import dataclass
from decimal import Decimal

from app.domain.errors import ValidationError


@dataclass(frozen=True)
class Price:
    """Represents a monetary amount.

    Args:
        amount: The price value. Must be non-negative.

    Raises:
        ValidationError: If amount is negative.
    """

    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValidationError("Price cannot be negative")
