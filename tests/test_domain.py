"""Unit tests for domain models and value objects (no DB, no HTTP)."""

from decimal import Decimal

import pytest

from app.domain.enums import OrderStatus, Role
from app.domain.errors import NotFoundError, ValidationError
from app.domain.models.cart import Cart
from app.domain.models.cart_item import CartItem
from app.domain.models.product import Product
from app.domain.value_objects.price import Price
from app.domain.value_objects.quantity import Quantity


def _make_product(*, product_id: str = "p1", price: Decimal = Decimal("10.00")) -> Product:
    return Product(
        id=product_id,
        name="Test",
        description="Desc",
        price=Price(amount=price),
        stock=Quantity(value=10),
        image_url="",
        category="",
    )


class TestPrice:
    """Tests for the Price value object."""

    def test_accepts_positive_decimal(self) -> None:
        p = Price(amount=Decimal("9.99"))
        assert p.amount == Decimal("9.99")

    def test_accepts_zero(self) -> None:
        p = Price(amount=Decimal(0))
        assert p.amount == Decimal(0)

    def test_rejects_negative(self) -> None:
        with pytest.raises(ValidationError, match="negative"):
            Price(amount=Decimal("-1"))


class TestQuantity:
    """Tests for the Quantity value object."""

    def test_accepts_positive(self) -> None:
        q = Quantity(value=5)
        assert q.value == 5

    def test_accepts_zero(self) -> None:
        q = Quantity(value=0)
        assert q.value == 0

    def test_rejects_negative(self) -> None:
        with pytest.raises(ValidationError, match="negative"):
            Quantity(value=-1)


class TestCart:
    """Tests for Cart domain logic."""

    def test_add_item_merges_same_product(self) -> None:
        """Adding the same product twice merges quantities."""
        cart = Cart(id="c1", user_id="u1")
        product = _make_product()
        cart.add_item(CartItem(product_id="p1", product=product, quantity=Quantity(2)))
        cart.add_item(CartItem(product_id="p1", product=product, quantity=Quantity(3)))
        assert len(cart.items) == 1
        assert cart.items[0].quantity.value == 5

    def test_add_item_different_products(self) -> None:
        """Adding different products creates separate items."""
        cart = Cart(id="c1", user_id="u1")
        cart.add_item(CartItem(product_id="p1", product=_make_product(product_id="p1"), quantity=Quantity(1)))
        cart.add_item(CartItem(product_id="p2", product=_make_product(product_id="p2"), quantity=Quantity(1)))
        assert len(cart.items) == 2

    def test_remove_item_raises_not_found(self) -> None:
        """Removing a non-existent item raises NotFoundError."""
        cart = Cart(id="c1", user_id="u1")
        with pytest.raises(NotFoundError):
            cart.remove_item("nonexistent")

    def test_remove_item_success(self) -> None:
        """Removing an existing item works."""
        cart = Cart(id="c1", user_id="u1")
        cart.add_item(CartItem(product_id="p1", product=_make_product(), quantity=Quantity(1)))
        cart.remove_item("p1")
        assert len(cart.items) == 0

    def test_update_item_quantity_zero_removes(self) -> None:
        """Updating quantity to zero removes the item."""
        cart = Cart(id="c1", user_id="u1")
        cart.add_item(CartItem(product_id="p1", product=_make_product(), quantity=Quantity(3)))
        cart.update_item_quantity("p1", Quantity(0))
        assert len(cart.items) == 0

    def test_update_item_quantity_success(self) -> None:
        """Updating quantity of an existing item works."""
        cart = Cart(id="c1", user_id="u1")
        cart.add_item(CartItem(product_id="p1", product=_make_product(), quantity=Quantity(1)))
        cart.update_item_quantity("p1", Quantity(7))
        assert cart.items[0].quantity.value == 7

    def test_total_calculates_correctly(self) -> None:
        """Total is computed as sum of price * quantity for all items."""
        cart = Cart(id="c1", user_id="u1")
        cart.add_item(CartItem(
            product_id="p1",
            product=_make_product(price=Decimal("10.00")),
            quantity=Quantity(2),
        ))
        cart.add_item(CartItem(
            product_id="p2",
            product=_make_product(product_id="p2", price=Decimal("5.50")),
            quantity=Quantity(3),
        ))
        assert cart.total == Decimal("36.50")

    def test_total_with_empty_cart(self) -> None:
        """Total of an empty cart is zero."""
        cart = Cart(id="c1", user_id="u1")
        assert cart.total == Decimal(0)


class TestEnums:
    """Tests for domain enumerations."""

    def test_role_values(self) -> None:
        assert Role.CUSTOMER == "customer"
        assert Role.ADMIN == "admin"

    def test_order_status_values(self) -> None:
        assert OrderStatus.PENDING == "pending"
        assert OrderStatus.CONFIRMED == "confirmed"
        assert OrderStatus.SHIPPED == "shipped"
        assert OrderStatus.DELIVERED == "delivered"
        assert OrderStatus.CANCELLED == "cancelled"
