"""Interface for order persistence operations."""

from abc import ABC, abstractmethod

from app.domain.models.order import Order


class OrderRepository(ABC):
    """Abstract repository for order data access."""

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> list[Order]:
        """Find all orders belonging to a user.

        Args:
            user_id: The user's UUID string.

        Returns:
            A list of Order domain objects.
        """
        ...

    @abstractmethod
    async def find_by_id(self, order_id: str) -> Order | None:
        """Find an order by its unique identifier.

        Args:
            order_id: The order's UUID string.

        Returns:
            The Order if found, None otherwise.
        """
        ...

    @abstractmethod
    async def save(self, order: Order) -> Order:
        """Persist an order (insert or update).

        Args:
            order: The order domain object to save.

        Returns:
            The saved order.
        """
        ...
