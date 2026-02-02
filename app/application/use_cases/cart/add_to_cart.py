"""Use case for adding a product to the shopping cart."""

import uuid
from dataclasses import dataclass

from app.application.interfaces.cart_repository import CartRepository
from app.application.interfaces.product_repository import ProductRepository
from app.domain.errors import NotFoundError
from app.domain.models.cart import Cart
from app.domain.models.cart_item import CartItem
from app.domain.value_objects.quantity import Quantity


@dataclass
class AddToCartInput:
    """Input data for adding an item to the cart.

    Attributes:
        user_id: The user's UUID string.
        product_id: The product's UUID string.
        quantity: Number of units to add.
    """

    user_id: str
    product_id: str
    quantity: int = 1


class AddToCart:
    """Adds a product to the user's shopping cart.

    Args:
        cart_repo: Repository for cart data access.
        product_repo: Repository for product data access.
    """

    def __init__(self, cart_repo: CartRepository, product_repo: ProductRepository) -> None:
        self._cart_repo = cart_repo
        self._product_repo = product_repo

    async def execute(self, input_data: AddToCartInput) -> Cart:
        """Execute the add to cart use case.

        Args:
            input_data: Details of the item to add.

        Returns:
            The updated Cart.

        Raises:
            NotFoundError: If the product does not exist.
        """
        product = await self._product_repo.find_by_id(input_data.product_id)
        if not product:
            raise NotFoundError(f"Product {input_data.product_id} not found")

        cart = await self._cart_repo.find_by_user_id(input_data.user_id)
        if not cart:
            cart = Cart(id=str(uuid.uuid4()), user_id=input_data.user_id, items=[])

        cart.add_item(CartItem(
            product_id=input_data.product_id,
            product=product,
            quantity=Quantity(input_data.quantity),
        ))

        await self._cart_repo.save(cart)
        return cart
