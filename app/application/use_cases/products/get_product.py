"""Use case for retrieving a single product."""

from app.application.interfaces.product_repository import ProductRepository
from app.domain.errors import NotFoundError
from app.domain.models.product import Product


class GetProduct:
    """Retrieves a product by its unique identifier.

    Args:
        product_repo: Repository for product data access.
    """

    def __init__(self, product_repo: ProductRepository) -> None:
        self._product_repo = product_repo

    async def execute(self, product_id: str) -> Product:
        """Execute the get product use case.

        Args:
            product_id: The product's UUID string.

        Returns:
            The requested Product.

        Raises:
            NotFoundError: If no product exists with the given ID.
        """
        product = await self._product_repo.find_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product {product_id} not found")
        return product
