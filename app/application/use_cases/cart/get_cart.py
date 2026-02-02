"""Use case for retrieving a user's shopping cart."""

import uuid

from app.application.interfaces.cart_repository import CartRepository
from app.domain.models.cart import Cart


class GetCart:
    """Retrieves the shopping cart for a given user.

    Args:
        cart_repo: Repository for cart data access.
    """

    def __init__(self, cart_repo: CartRepository) -> None:
        self._cart_repo = cart_repo

    async def execute(self, user_id: str) -> Cart:
        """Execute the get cart use case.

        Args:
            user_id: The user's UUID string.

        Returns:
            The user's Cart, or an empty Cart if none exists.
        """
        cart = await self._cart_repo.find_by_user_id(user_id)
        if not cart:
            return Cart(id=str(uuid.uuid4()), user_id=user_id, items=[])
        return cart
