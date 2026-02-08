"""Product domain model."""

from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.price import Price
from app.domain.value_objects.quantity import Quantity


@dataclass
class Product:
    """Represents a product available for purchase.

    Attributes:
        id: Unique identifier.
        name: Product name.
        description: Detailed product description.
        price: Product price as a Price value object.
        stock: Available stock as a Quantity value object.
        image_url: URL to the product image.
        category: Product category (e.g., clothing, shoes).
        parent_category: Parent category (e.g., women, men, sale).
        created_at: Timestamp of creation.
    """

    id: str
    name: str
    description: str
    price: Price
    stock: Quantity
    image_url: str
    category: str
    parent_category: str
    created_at: datetime | None = None
