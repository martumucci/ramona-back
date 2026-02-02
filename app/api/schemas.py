"""Pydantic request/response schemas for the API layer."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


def to_camel(s: str) -> str:
    """Convert a snake_case string to camelCase."""
    parts = s.split("_")
    return parts[0] + "".join(w.capitalize() for w in parts[1:])


class CamelModel(BaseModel):
    """Base model with automatic camelCase alias generation."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


# --- Auth ---


class RegisterRequest(CamelModel):
    """Request body for user registration."""

    email: EmailStr
    name: str
    password: str


class LoginRequest(CamelModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class AuthResponse(CamelModel):
    """Response for successful authentication."""

    access_token: str
    token_type: str
    user_id: str
    name: str


# --- Products ---


class ProductResponse(CamelModel):
    """Response representing a product."""

    id: str
    name: str
    description: str
    price: Decimal
    stock: int
    image_url: str
    category: str
    created_at: datetime | None = None


# --- Cart ---


class CartItemResponse(CamelModel):
    """Response representing a single cart item."""

    product_id: str
    name: str
    price: Decimal
    image_url: str
    quantity: int
    subtotal: Decimal


class CartResponse(CamelModel):
    """Response representing a user's shopping cart."""

    id: str
    items: list[CartItemResponse]
    total: Decimal


class AddToCartRequest(CamelModel):
    """Request body for adding an item to the cart."""

    product_id: str
    quantity: int = 1


class UpdateCartItemRequest(CamelModel):
    """Request body for updating a cart item's quantity."""

    quantity: int
