"""Interface for product persistence operations."""

from abc import ABC, abstractmethod

from app.domain.models.product import Product


class ProductRepository(ABC):
    """Abstract repository for product data access."""

    @abstractmethod
    async def find_all(self, *, offset: int = 0, limit: int | None = None) -> list[Product]:
        """Retrieve all products with optional pagination.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return. None means no limit.

        Returns:
            A list of Product domain objects.
        """
        ...

    @abstractmethod
    async def find_by_id(self, product_id: str) -> Product | None:
        """Find a product by its unique identifier.

        Args:
            product_id: The product's UUID string.

        Returns:
            The Product if found, None otherwise.
        """
        ...

    @abstractmethod
    async def save(self, product: Product) -> Product:
        """Persist a product (insert or update).

        Args:
            product: The product domain object to save.

        Returns:
            The saved product.
        """
        ...

    @abstractmethod
    async def get_categories(self) -> dict[str, list[str]]:
        """Retrieve all categories grouped by parent category.

        Returns:
            A dict mapping parent categories to their child categories.
        """
        ...
