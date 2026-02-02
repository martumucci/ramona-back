"""Use case for updating a cart item's quantity."""

from dataclasses import dataclass

from app.application.interfaces.cart_repository import CartRepository
from app.domain.errors import NotFoundError
from app.domain.models.cart import Cart
from app.domain.value_objects.quantity import Quantity


@dataclass
class UpdateCartItemInput:
    """Input data for updating a cart item.

    Attributes:
        user_id: The user's UUID string.
        product_id: The product's UUID string.
        quantity: The new quantity.
    """

    user_id: str
    product_id: str
    quantity: int


class UpdateCartItem:
    """Updates the quantity of an item in the user's shopping cart.

    Args:
        cart_repo: Repository for cart data access.
    """

    def __init__(self, cart_repo: CartRepository) -> None:
        self._cart_repo = cart_repo

    async def execute(self, input_data: UpdateCartItemInput) -> Cart:
        """Execute the update cart item use case.

        Args:
            input_data: The update details.

        Returns:
            The updated Cart.

        Raises:
            NotFoundError: If the cart does not exist.
        """
        cart = await self._cart_repo.find_by_user_id(input_data.user_id)
        if not cart:
            raise NotFoundError("Cart not found")

        cart.update_item_quantity(input_data.product_id, Quantity(input_data.quantity))
        await self._cart_repo.save(cart)
        return cart
