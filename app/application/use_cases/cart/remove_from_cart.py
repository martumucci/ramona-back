"""Use case for removing a product from the shopping cart."""

from app.application.interfaces.cart_repository import CartRepository
from app.domain.errors import NotFoundError
from app.domain.models.cart import Cart


class RemoveFromCart:
    """Removes a product from the user's shopping cart.

    Args:
        cart_repo: Repository for cart data access.
    """

    def __init__(self, cart_repo: CartRepository) -> None:
        self._cart_repo = cart_repo

    async def execute(self, user_id: str, product_id: str) -> Cart:
        """Execute the remove from cart use case.

        Args:
            user_id: The user's UUID string.
            product_id: The product's UUID string to remove.

        Returns:
            The updated Cart.

        Raises:
            NotFoundError: If the cart or item does not exist.
        """
        cart = await self._cart_repo.find_by_user_id(user_id)
        if not cart:
            raise NotFoundError("Cart not found")

        cart.remove_item(product_id)
        await self._cart_repo.save(cart)
        return cart
