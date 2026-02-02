"""Shared test fixtures for the Ramona Shop test suite."""

from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.infrastructure.db.base import Base

# Import all models so they register with metadata
from app.infrastructure.db.models.cart_model import CartItemModel, CartModel  # noqa: F401
from app.infrastructure.db.models.order_model import OrderItemModel, OrderModel  # noqa: F401
from app.infrastructure.db.models.product_model import ProductModel  # noqa: F401
from app.infrastructure.db.models.user_model import UserModel  # noqa: F401

TEST_DATABASE_URL = "sqlite+aiosqlite://"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    """Create and tear down the test database schema for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a clean database session for direct DB operations in tests."""
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an HTTP test client with dependency overrides."""
    from app.api.dependencies import get_session
    from app.main import app

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        async with TestingSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_token(client: AsyncClient) -> str:
    """Register a test user and return a valid access token."""
    response = await client.post("/api/auth/register", json={
        "email": "fixture@test.com",
        "name": "Fixture User",
        "password": "password123",
    })
    data = response.json()
    return data["accessToken"]
