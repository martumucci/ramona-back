"""SQLAlchemy implementation of the CartRepository."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.cart_repository import CartRepository
from app.domain.models.cart import Cart
from app.domain.models.cart_item import CartItem
from app.domain.models.product import Product
from app.domain.value_objects.price import Price
from app.domain.value_objects.quantity import Quantity
from app.infrastructure.db.models.cart_model import CartItemModel, CartModel
from app.infrastructure.db.utils import parse_uuid


class SqlAlchemyCartRepository(CartRepository):
    """Persists Cart domain objects using SQLAlchemy.

    Args:
        session: An async SQLAlchemy session.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_user_id(self, user_id: str) -> Cart | None:
        """Find a cart by the owning user's ID.

        Args:
            user_id: The user's UUID string.

        Returns:
            The Cart if found, None otherwise.
        """
        result = await self._session.execute(
            select(CartModel).where(CartModel.user_id == parse_uuid(user_id))
        )
        model = result.scalar_one_or_none()
        if not model:
            return None
        return self._to_domain(model)

    async def save(self, cart: Cart) -> Cart:
        """Persist a cart (insert or update).

        Args:
            cart: The cart domain object to save.

        Returns:
            The saved cart.
        """
        result = await self._session.execute(
            select(CartModel).where(CartModel.user_id == parse_uuid(cart.user_id))
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.items.clear()
            await self._session.flush()
            for item in cart.items:
                existing.items.append(CartItemModel(
                    id=uuid.uuid4(),
                    cart_id=existing.id,
                    product_id=parse_uuid(item.product_id),
                    quantity=item.quantity.value,
                ))
            await self._session.flush()
            await self._session.refresh(existing)
            return self._to_domain(existing)
        else:
            cart_id = parse_uuid(cart.id) if cart.id else uuid.uuid4()
            model = CartModel(
                id=cart_id,
                user_id=parse_uuid(cart.user_id),
                items=[
                    CartItemModel(
                        id=uuid.uuid4(),
                        cart_id=cart_id,
                        product_id=parse_uuid(item.product_id),
                        quantity=item.quantity.value,
                    )
                    for item in cart.items
                ],
            )
            self._session.add(model)
            await self._session.flush()
            await self._session.refresh(model)
            return self._to_domain(model)

    @staticmethod
    def _to_domain(model: CartModel) -> Cart:
        items = []
        for ci in model.items:
            product = None
            if ci.product:
                product = Product(
                    id=str(ci.product.id),
                    name=ci.product.name,
                    description=ci.product.description,
                    price=Price(amount=Decimal(str(ci.product.price))),
                    stock=Quantity(value=ci.product.stock),
                    image_url=ci.product.image_url,
                    category=ci.product.category,
                    created_at=ci.product.created_at,
                )
            items.append(CartItem(
                product_id=str(ci.product_id),
                product=product,
                quantity=Quantity(ci.quantity),
            ))
        return Cart(id=str(model.id), user_id=str(model.user_id), items=items)
