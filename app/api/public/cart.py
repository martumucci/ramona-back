"""Shopping cart route handlers."""

from fastapi import APIRouter

from app.api.dependencies import (
    AddToCartDep,
    GetCartDep,
    OptionalUserId,
    RemoveFromCartDep,
    UpdateCartItemDep,
)
from app.api.mappers import cart_to_response
from app.api.schemas import AddToCartRequest, CartResponse, UpdateCartItemRequest
from app.application.use_cases.cart.add_to_cart import AddToCartInput
from app.application.use_cases.cart.update_cart_item import UpdateCartItemInput

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartResponse)
async def get_cart(user_id: OptionalUserId, use_case: GetCartDep) -> CartResponse:
    """Get the current user's shopping cart."""
    cart = await use_case.execute(user_id)
    return cart_to_response(cart)


@router.post("/items", response_model=CartResponse)
async def add_item(
    body: AddToCartRequest, user_id: OptionalUserId, use_case: AddToCartDep
) -> CartResponse:
    """Add a product to the shopping cart."""
    cart = await use_case.execute(AddToCartInput(
        user_id=user_id,
        product_id=body.product_id,
        quantity=body.quantity,
    ))
    return cart_to_response(cart)


@router.patch("/items/{product_id}", response_model=CartResponse)
async def update_item(
    product_id: str,
    body: UpdateCartItemRequest,
    user_id: OptionalUserId,
    use_case: UpdateCartItemDep,
) -> CartResponse:
    """Update the quantity of a cart item."""
    cart = await use_case.execute(UpdateCartItemInput(
        user_id=user_id,
        product_id=product_id,
        quantity=body.quantity,
    ))
    return cart_to_response(cart)


@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_item(
    product_id: str, user_id: OptionalUserId, use_case: RemoveFromCartDep
) -> CartResponse:
    """Remove an item from the shopping cart."""
    cart = await use_case.execute(user_id, product_id)
    return cart_to_response(cart)
