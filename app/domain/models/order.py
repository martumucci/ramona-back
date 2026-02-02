"""Order domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.domain.enums import OrderStatus
from app.domain.models.cart_item import CartItem


@dataclass
class Order:
    """Represents a placed order.

    Attributes:
        id: Unique identifier.
        user_id: ID of the user who placed the order.
        items: List of ordered items.
        total: Total price of the order.
        status: Current order status.
        created_at: Timestamp of creation.
    """

    id: str
    user_id: str
    items: list[CartItem] = field(default_factory=list)
    total: Decimal = Decimal(0)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime | None = None
