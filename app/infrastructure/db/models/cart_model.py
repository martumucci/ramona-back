import uuid

from sqlalchemy import ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base
from app.infrastructure.db.models.product_model import ProductModel  # noqa: F401


class CartModel(Base):
    __tablename__ = "carts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("users.id"), unique=True, nullable=False)
    items: Mapped[list["CartItemModel"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan", lazy="selectin"
    )


class CartItemModel(Base):
    __tablename__ = "cart_items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    cart_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    cart: Mapped["CartModel"] = relationship(back_populates="items")
    product: Mapped["ProductModel"] = relationship(lazy="selectin")
