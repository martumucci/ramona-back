"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient) -> None:
    """Registering a new user returns a valid access token."""
    response = await client.post("/api/auth/register", json={
        "email": "newuser@test.com",
        "name": "New User",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["accessToken"]
    assert data["tokenType"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    """Registering with an existing email returns 422."""
    payload = {"email": "dup@test.com", "name": "User", "password": "pass123"}
    await client.post("/api/auth/register", json=payload)
    response = await client.post("/api/auth/register", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login(client: AsyncClient) -> None:
    """Logging in with valid credentials returns a valid access token."""
    await client.post("/api/auth/register", json={
        "email": "login@test.com",
        "name": "Login User",
        "password": "password123",
    })
    response = await client.post("/api/auth/login", json={
        "email": "login@test.com",
        "password": "password123",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["accessToken"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    """Logging in with invalid credentials returns 401."""
    response = await client.post("/api/auth/login", json={
        "email": "nonexistent@test.com",
        "password": "wrong",
    })
    assert response.status_code == 401
