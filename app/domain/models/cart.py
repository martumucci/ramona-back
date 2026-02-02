"""Shopping cart domain model."""

from dataclasses import dataclass, field
from decimal import Decimal

from app.domain.errors import NotFoundError, ValidationError
from app.domain.models.cart_item import CartItem
from app.domain.value_objects.quantity import Quantity


@dataclass
class Cart:
    """Represents a user's shopping cart.

    Attributes:
        id: Unique identifier.
        user_id: ID of the owning user.
        items: List of cart items.
    """

    id: str
    user_id: str
    items: list[CartItem] = field(default_factory=list)

    def add_item(self, item: CartItem) -> None:
        """Add an item to the cart, merging quantities if the product already exists.

        Args:
            item: The cart item to add.
        """
        for existing in self.items:
            if existing.product_id == item.product_id:
                existing.quantity = Quantity(existing.quantity.value + item.quantity.value)
                return
        self.items.append(item)

    def remove_item(self, product_id: str) -> None:
        """Remove an item from the cart by product ID.

        Args:
            product_id: The product ID to remove.

        Raises:
            NotFoundError: If the product is not in the cart.
        """
        original_len = len(self.items)
        self.items = [i for i in self.items if i.product_id != product_id]
        if len(self.items) == original_len:
            raise NotFoundError(f"Item with product_id {product_id} not found in cart")

    def update_item_quantity(self, product_id: str, quantity: Quantity) -> None:
        """Update the quantity of an existing cart item.

        Args:
            product_id: The product ID to update.
            quantity: The new quantity. If zero, the item is removed.

        Raises:
            ValidationError: If quantity is negative.
            NotFoundError: If the product is not in the cart.
        """
        if quantity.value < 0:
            raise ValidationError("Quantity cannot be negative")
        if quantity.value == 0:
            self.remove_item(product_id)
            return
        for item in self.items:
            if item.product_id == product_id:
                item.quantity = quantity
                return
        raise NotFoundError(f"Item with product_id {product_id} not found in cart")

    @property
    def total(self) -> Decimal:
        """Calculate the total price of all items in the cart.

        Returns:
            The sum of price * quantity for all items with loaded products.
        """
        return sum(
            (item.product.price.amount * item.quantity.value
             for item in self.items
             if item.product is not None),
            Decimal(0),
        )
