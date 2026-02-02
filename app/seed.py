"""Database seed script for initial development data."""

import asyncio
import uuid

from sqlalchemy import select

from app.infrastructure.auth.password_hasher import PasswordHasher
from app.infrastructure.db.models.product_model import ProductModel
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.session import async_session

_SEED_USERS = [
    {"email": "admin@ramona.com", "name": "Admin", "password": "admin123", "role": "admin"},
    {"email": "test@ramona.com", "name": "Test User", "password": "test123", "role": "customer"},
]

_SEED_PRODUCTS = [
    {
        "name": "Classic White T-Shirt",
        "description": "Essential cotton t-shirt in classic white. Soft, breathable fabric perfect for everyday wear.",
        "price": 29.99,
        "stock": 100,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        "category": "T-Shirts",
    },
    {
        "name": "Black Graphic Tee",
        "description": "Bold graphic print on premium black cotton. Stand out with this modern design.",
        "price": 34.99,
        "stock": 75,
        "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400",
        "category": "T-Shirts",
    },
    {
        "name": "Slim Fit Jeans",
        "description": "Modern slim fit jeans in classic indigo wash. Stretch denim for comfort.",
        "price": 59.99,
        "stock": 60,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        "category": "Pants",
    },
    {
        "name": "Casual Hoodie",
        "description": "Cozy pullover hoodie in heather gray. Perfect for layering in cooler weather.",
        "price": 49.99,
        "stock": 80,
        "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",
        "category": "Hoodies",
    },
    {
        "name": "Leather Sneakers",
        "description": "Premium leather sneakers with cushioned sole. Clean minimal design.",
        "price": 89.99,
        "stock": 45,
        "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400",
        "category": "Shoes",
    },
    {
        "name": "Denim Jacket",
        "description": "Classic denim jacket with button closure. Vintage-inspired wash.",
        "price": 79.99,
        "stock": 35,
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400",
        "category": "Jackets",
    },
    {
        "name": "Striped Polo Shirt",
        "description": "Navy and white striped polo in breathable pique cotton.",
        "price": 39.99,
        "stock": 90,
        "image_url": "https://images.unsplash.com/photo-1625910513413-5fc42f2aec71?w=400",
        "category": "T-Shirts",
    },
    {
        "name": "Chino Pants",
        "description": "Tailored chino pants in khaki. Versatile style for work or weekend.",
        "price": 54.99,
        "stock": 55,
        "image_url": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400",
        "category": "Pants",
    },
    {
        "name": "Canvas Backpack",
        "description": "Durable canvas backpack with leather accents. Multiple compartments.",
        "price": 69.99,
        "stock": 40,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
        "category": "Accessories",
    },
    {
        "name": "Wool Beanie",
        "description": "Soft merino wool beanie in charcoal. Warm and stylish for cold days.",
        "price": 24.99,
        "stock": 120,
        "image_url": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=400",
        "category": "Accessories",
    },
    {
        "name": "Running Shoes",
        "description": "Lightweight running shoes with responsive cushioning. Breathable mesh upper.",
        "price": 109.99,
        "stock": 50,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "category": "Shoes",
    },
    {
        "name": "Linen Summer Shirt",
        "description": "Relaxed fit linen shirt in light blue. Perfect for warm weather.",
        "price": 44.99,
        "stock": 65,
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
        "category": "T-Shirts",
    },
]


async def seed() -> None:
    """Populate the database with initial development data.

    Creates default users and sample products if they don't already exist.
    Passwords are hashed at insertion time, not at module import.
    """
    hasher = PasswordHasher()

    async with async_session() as session:
        # Seed users
        for user_data in _SEED_USERS:
            existing = await session.execute(
                select(UserModel).where(UserModel.email == user_data["email"])
            )
            if not existing.scalar_one_or_none():
                session.add(UserModel(
                    id=uuid.uuid4(),
                    email=user_data["email"],
                    name=user_data["name"],
                    hashed_password=hasher.hash(user_data["password"]),
                    role=user_data["role"],
                ))
                print(f"  Created user: {user_data['email']}")

        # Seed products
        for product_data in _SEED_PRODUCTS:
            existing = await session.execute(
                select(ProductModel).where(ProductModel.name == product_data["name"])
            )
            if not existing.scalar_one_or_none():
                session.add(ProductModel(id=uuid.uuid4(), **product_data))
                print(f"  Created product: {product_data['name']}")

        await session.commit()
        print("Seed completed!")


if __name__ == "__main__":
    asyncio.run(seed())
