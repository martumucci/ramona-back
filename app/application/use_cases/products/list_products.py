"""Use case for listing products with optional pagination."""

from app.application.interfaces.product_repository import ProductRepository
from app.domain.models.product import Product


class ListProducts:
    """Retrieves a paginated list of products.

    Args:
        product_repo: Repository for product data access.
    """

    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(
        self, *, offset: int = 0, limit: int | None = None
    ) -> list[Product]:
        """Execute the list products use case.

        Args:
            offset: Number of products to skip.
            limit: Maximum number of products to return.

        Returns:
            A list of Product domain objects.
        """
        return await self._product_repo.find_all(offset=offset, limit=limit)
