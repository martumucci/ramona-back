"""Mappers from domain models to API response schemas."""

from decimal import Decimal

from app.api.schemas import CartItemResponse, CartResponse, ProductResponse
from app.domain.models.cart import Cart
from app.domain.models.product import Product


def product_to_response(product: Product) -> ProductResponse:
    """Map a Product domain model to a ProductResponse schema.

    Args:
        product: The product domain object.

    Returns:
        A ProductResponse Pydantic model.
    """
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price.amount,
        stock=product.stock.value,
        image_url=product.image_url,
        category=product.category,
        parent_category=product.parent_category,
        created_at=product.created_at,
    )


def cart_to_response(cart: Cart) -> CartResponse:
    """Map a Cart domain model to a CartResponse schema.

    Args:
        cart: The cart domain object.

    Returns:
        A CartResponse Pydantic model.
    """
    items: list[CartItemResponse] = []
    for item in cart.items:
        price = item.product.price.amount if item.product else Decimal(0)
        name = item.product.name if item.product else ""
        image_url = item.product.image_url if item.product else ""
        items.append(CartItemResponse(
            product_id=item.product_id,
            name=name,
            price=price,
            image_url=image_url,
            quantity=item.quantity.value,
            subtotal=price * item.quantity.value,
        ))
    return CartResponse(
        id=cart.id,
        items=items,
        total=cart.total,
    )
