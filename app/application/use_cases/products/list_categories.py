"""Use case for listing product categories."""

from app.application.interfaces.product_repository import ProductRepository


class ListCategories:
    """Retrieves all unique product categories.

    Args:
        product_repo: Repository for product data access.
    """

    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(self) -> dict[str, list[str]]:
        """Execute the list categories use case.

        Returns:
            A dict mapping parent categories to their child categories.
        """
        return await self._product_repo.get_categories()
