"""SQLAlchemy implementation of the ProductRepository."""

from decimal import Decimal

from sqlalchemy import distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.product_repository import ProductRepository
from app.domain.models.product import Product
from app.domain.value_objects.price import Price
from app.domain.value_objects.quantity import Quantity
from app.infrastructure.db.models.product_model import ProductModel
from app.infrastructure.db.utils import parse_uuid


class SqlAlchemyProductRepository(ProductRepository):
    """Persists Product domain objects using SQLAlchemy.

    Args:
        session: An async SQLAlchemy session.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self, *, offset: int = 0, limit: int | None = None) -> list[Product]:
        """Retrieve all products with optional pagination.

        Args:
            offset: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            A list of Product domain objects.
        """
        stmt = select(ProductModel).order_by(ProductModel.created_at).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self._session.execute(stmt)
        return [self._to_domain(row) for row in result.scalars().all()]

    async def find_by_id(self, product_id: str) -> Product | None:
        """Find a product by its unique identifier.

        Args:
            product_id: The product's UUID string.

        Returns:
            The Product if found, None otherwise.
        """
        result = await self._session.execute(
            select(ProductModel).where(ProductModel.id == parse_uuid(product_id))
        )
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def save(self, product: Product) -> Product:
        """Persist a product (insert or update).

        Args:
            product: The product domain object to save.

        Returns:
            The saved product.
        """
        model = ProductModel(
            id=parse_uuid(product.id),
            name=product.name,
            description=product.description,
            price=product.price.amount,
            stock=product.stock.value,
            image_url=product.image_url,
            category=product.category,
            parent_category=product.parent_category,
        )
        merged = await self._session.merge(model)
        await self._session.flush()
        return self._to_domain(merged)

    async def get_categories(self) -> dict[str, list[str]]:
        """Retrieve all categories grouped by parent category.

        Returns:
            A dict mapping parent categories to their child categories.
        """
        result = await self._session.execute(
            select(
                ProductModel.parent_category,
                ProductModel.category
            ).distinct().order_by(
                ProductModel.parent_category,
                ProductModel.category
            )
        )
        categories: dict[str, list[str]] = {}
        for parent, child in result.all():
            if parent not in categories:
                categories[parent] = []
            if child not in categories[parent]:
                categories[parent].append(child)
        return categories

    @staticmethod
    def _to_domain(model: ProductModel) -> Product:
        return Product(
            id=str(model.id),
            name=model.name,
            description=model.description,
            price=Price(amount=Decimal(str(model.price))),
            stock=Quantity(value=model.stock),
            image_url=model.image_url,
            category=model.category,
            parent_category=model.parent_category,
            created_at=model.created_at,
        )
