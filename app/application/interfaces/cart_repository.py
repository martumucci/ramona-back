"""Interface for cart persistence operations."""

from abc import ABC, abstractmethod

from app.domain.models.cart import Cart


class CartRepository(ABC):
    """Abstract repository for shopping cart data access."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Cart | None:
        """Find a cart by the owning user's ID.

        Args:
            user_id: The user's UUID string.

        Returns:
            The Cart if found, None otherwise.
        """
        ...

    @abstractmethod
    async def save(self, cart: Cart) -> Cart:
        """Persist a cart (insert or update).

        Args:
            cart: The cart domain object to save.

        Returns:
            The saved cart.
        """
        ...
