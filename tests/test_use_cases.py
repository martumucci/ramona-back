"""Unit tests for use cases with in-memory fakes (no DB, no HTTP)."""

import uuid
from decimal import Decimal

import pytest

from app.application.dtos import AuthResult
from app.application.interfaces.cart_repository import CartRepository
from app.application.interfaces.product_repository import ProductRepository
from app.application.interfaces.user_repository import UserRepository
from app.application.use_cases.auth.login_user import LoginUser, LoginUserInput
from app.application.use_cases.auth.register_user import RegisterUser, RegisterUserInput
from app.application.use_cases.cart.add_to_cart import AddToCart, AddToCartInput
from app.domain.errors import AuthenticationError, NotFoundError, ValidationError
from app.domain.models.cart import Cart
from app.domain.models.product import Product
from app.domain.models.user import User
from app.domain.value_objects.price import Price
from app.domain.value_objects.quantity import Quantity


# --- Fakes ---


class FakeUserRepository(UserRepository):
    """In-memory user repository for testing."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    async def find_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    async def find_by_id(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    async def save(self, user: User) -> User:
        self._users[user.id] = user
        return user


class FakeProductRepository(ProductRepository):
    """In-memory product repository for testing."""

    def __init__(self, products: list[Product] | None = None) -> None:
        self._products: dict[str, Product] = {}
        for p in products or []:
            self._products[p.id] = p

    async def find_all(self, *, offset: int = 0, limit: int | None = None) -> list[Product]:
        items = list(self._products.values())[offset:]
        if limit is not None:
            items = items[:limit]
        return items

    async def find_by_id(self, product_id: str) -> Product | None:
        return self._products.get(product_id)

    async def save(self, product: Product) -> Product:
        self._products[product.id] = product
        return product


class FakeCartRepository(CartRepository):
    """In-memory cart repository for testing."""

    def __init__(self) -> None:
        self._carts: dict[str, Cart] = {}

    async def find_by_user_id(self, user_id: str) -> Cart | None:
        return self._carts.get(user_id)

    async def save(self, cart: Cart) -> Cart:
        self._carts[cart.user_id] = cart
        return cart


class FakePasswordHasher:
    """Simple password hasher for testing (prefix-based)."""

    def hash(self, password: str) -> str:
        return f"hashed:{password}"

    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed:{plain}"


class FakeTokenGenerator:
    """Simple token generator for testing."""

    def generate(self, user_id: str) -> str:
        return f"token:{user_id}"

    def verify(self, token: str) -> str:
        return token.removeprefix("token:")


# --- RegisterUser Tests ---


class TestRegisterUser:
    """Tests for the RegisterUser use case."""

    @pytest.mark.asyncio
    async def test_happy_path(self) -> None:
        """Registering a new user succeeds and returns AuthResult."""
        repo = FakeUserRepository()
        uc = RegisterUser(repo, FakePasswordHasher(), FakeTokenGenerator())
        result = await uc.execute(RegisterUserInput(
            email="new@test.com",
            name="New",
            password="pass",
        ))
        assert isinstance(result, AuthResult)
        assert result.access_token.startswith("token:")
        assert result.name == "New"

    @pytest.mark.asyncio
    async def test_duplicate_email(self) -> None:
        """Registering with a taken email raises ValidationError."""
        repo = FakeUserRepository()
        uc = RegisterUser(repo, FakePasswordHasher(), FakeTokenGenerator())
        await uc.execute(RegisterUserInput(email="dup@test.com", name="A", password="p"))
        with pytest.raises(ValidationError, match="already registered"):
            await uc.execute(RegisterUserInput(email="dup@test.com", name="B", password="p"))


# --- LoginUser Tests ---


class TestLoginUser:
    """Tests for the LoginUser use case."""

    @pytest.mark.asyncio
    async def test_happy_path(self) -> None:
        """Logging in with correct credentials succeeds."""
        repo = FakeUserRepository()
        hasher = FakePasswordHasher()
        register_uc = RegisterUser(repo, hasher, FakeTokenGenerator())
        await register_uc.execute(RegisterUserInput(
            email="user@test.com",
            name="User",
            password="secret",
        ))

        login_uc = LoginUser(repo, hasher, FakeTokenGenerator())
        result = await login_uc.execute(LoginUserInput(
            email="user@test.com",
            password="secret",
        ))
        assert isinstance(result, AuthResult)

    @pytest.mark.asyncio
    async def test_wrong_password(self) -> None:
        """Logging in with wrong password raises AuthenticationError."""
        repo = FakeUserRepository()
        hasher = FakePasswordHasher()
        register_uc = RegisterUser(repo, hasher, FakeTokenGenerator())
        await register_uc.execute(RegisterUserInput(
            email="user@test.com",
            name="User",
            password="secret",
        ))

        login_uc = LoginUser(repo, hasher, FakeTokenGenerator())
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await login_uc.execute(LoginUserInput(email="user@test.com", password="wrong"))

    @pytest.mark.asyncio
    async def test_nonexistent_email(self) -> None:
        """Logging in with unknown email raises AuthenticationError."""
        uc = LoginUser(FakeUserRepository(), FakePasswordHasher(), FakeTokenGenerator())
        with pytest.raises(AuthenticationError, match="Invalid credentials"):
            await uc.execute(LoginUserInput(email="ghost@test.com", password="any"))


# --- AddToCart Tests ---


class TestAddToCart:
    """Tests for the AddToCart use case."""

    @pytest.mark.asyncio
    async def test_product_not_found(self) -> None:
        """Adding a non-existent product raises NotFoundError."""
        uc = AddToCart(FakeCartRepository(), FakeProductRepository())
        with pytest.raises(NotFoundError):
            await uc.execute(AddToCartInput(
                user_id="u1",
                product_id=str(uuid.uuid4()),
                quantity=1,
            ))

    @pytest.mark.asyncio
    async def test_add_successfully(self) -> None:
        """Adding an existing product creates a cart with the item."""
        product = Product(
            id="p1",
            name="Test",
            description="Desc",
            price=Price(amount=Decimal("10.00")),
            stock=Quantity(value=100),
            image_url="",
            category="",
        )
        product_repo = FakeProductRepository([product])
        cart_repo = FakeCartRepository()
        uc = AddToCart(cart_repo, product_repo)

        cart = await uc.execute(AddToCartInput(user_id="u1", product_id="p1", quantity=3))
        assert len(cart.items) == 1
        assert cart.items[0].quantity.value == 3
