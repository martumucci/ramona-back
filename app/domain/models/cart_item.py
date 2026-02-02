"""Cart item domain model."""

from dataclasses import dataclass

from app.domain.models.product import Product
from app.domain.value_objects.quantity import Quantity


@dataclass
class CartItem:
    """Represents a single item within a shopping cart.

    Attributes:
        product_id: ID of the associated product.
        product: Full product data (may be None if not loaded).
        quantity: Number of units as a Quantity value object.
    """

    product_id: str
    product: Product | None
    quantity: Quantity
