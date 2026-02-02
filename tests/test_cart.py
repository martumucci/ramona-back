"""Integration tests for the cart endpoints (full lifecycle)."""

import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.product_model import ProductModel


@pytest.fixture
async def product_id(session: AsyncSession) -> str:
    """Seed a product and return its ID for cart tests."""
    pid = uuid.uuid4()
    session.add(ProductModel(
        id=pid,
        name="Cart Test Product",
        description="Product for cart testing",
        price=Decimal("25.00"),
        stock=50,
        image_url="https://example.com/cart.jpg",
        category="Test",
    ))
    await session.commit()
    return str(pid)


@pytest.mark.asyncio
async def test_cart_full_lifecycle(
    client: AsyncClient, auth_token: str, product_id: str
) -> None:
    """Test the complete cart lifecycle: get empty -> add -> update -> remove -> verify empty."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Get empty cart
    response = await client.get("/api/cart", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []

    # Add item
    response = await client.post("/api/cart/items", headers=headers, json={
        "productId": product_id,
        "quantity": 2,
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2

    # Update quantity
    response = await client.patch(f"/api/cart/items/{product_id}", headers=headers, json={
        "quantity": 5,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["quantity"] == 5

    # Remove item
    response = await client.delete(f"/api/cart/items/{product_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []


@pytest.mark.asyncio
async def test_cart_requires_auth(client: AsyncClient) -> None:
    """Cart endpoints require authentication."""
    response = await client.get("/api/cart")
    assert response.status_code == 403
