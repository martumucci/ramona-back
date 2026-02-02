"""Tests for product endpoints."""

import uuid
from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.product_model import ProductModel


@pytest.mark.asyncio
async def test_list_products_empty(client: AsyncClient) -> None:
    """Listing products with no data returns an empty list."""
    response = await client.get("/api/products")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_products(client: AsyncClient, session: AsyncSession) -> None:
    """Listing products returns seeded products."""
    product = ProductModel(
        id=uuid.uuid4(),
        name="Test Product",
        description="A test product",
        price=Decimal("19.99"),
        stock=10,
        image_url="https://example.com/img.jpg",
        category="Test",
    )
    session.add(product)
    await session.commit()

    response = await client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Product"


@pytest.mark.asyncio
async def test_list_products_with_pagination(client: AsyncClient, session: AsyncSession) -> None:
    """Listing products with limit/offset works correctly."""
    for i in range(5):
        session.add(ProductModel(
            id=uuid.uuid4(),
            name=f"Product {i}",
            description=f"Description {i}",
            price=Decimal("10.00"),
            stock=10,
            image_url="https://example.com/img.jpg",
            category="Test",
        ))
    await session.commit()

    response = await client.get("/api/products?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_product(client: AsyncClient, session: AsyncSession) -> None:
    """Getting a product by ID returns its details."""
    pid = uuid.uuid4()
    product = ProductModel(
        id=pid,
        name="Detail Product",
        description="Product detail test",
        price=Decimal("29.99"),
        stock=5,
        image_url="https://example.com/detail.jpg",
        category="Detail",
    )
    session.add(product)
    await session.commit()

    response = await client.get(f"/api/products/{pid}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Detail Product"


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient) -> None:
    """Getting a non-existent product returns 404."""
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/products/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    """Health check endpoint returns ok."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
