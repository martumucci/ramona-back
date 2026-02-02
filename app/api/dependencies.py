"""FastAPI dependency injection configuration."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.cart_repository import CartRepository
from app.application.interfaces.password_hasher import PasswordHasher
from app.application.interfaces.product_repository import ProductRepository
from app.application.interfaces.token_generator import TokenGenerator
from app.application.interfaces.user_repository import UserRepository
from app.application.use_cases.auth.login_user import LoginUser
from app.application.use_cases.auth.register_user import RegisterUser
from app.application.use_cases.cart.add_to_cart import AddToCart
from app.application.use_cases.cart.get_cart import GetCart
from app.application.use_cases.cart.remove_from_cart import RemoveFromCart
from app.application.use_cases.cart.update_cart_item import UpdateCartItem
from app.application.use_cases.products.get_product import GetProduct
from app.application.use_cases.products.list_products import ListProducts
from app.config import settings
from app.domain.enums import Role
from app.domain.errors import AuthorizationError
from app.infrastructure.auth.password_hasher import PasswordHasher as PasswordHasherImpl
from app.infrastructure.auth.token_generator import TokenGenerator as TokenGeneratorImpl
from app.infrastructure.db.session import async_session
from app.infrastructure.repositories.cart_repository_impl import SqlAlchemyCartRepository
from app.infrastructure.repositories.product_repository_impl import SqlAlchemyProductRepository
from app.infrastructure.repositories.user_repository_impl import SqlAlchemyUserRepository

_security = HTTPBearer()

# Singletons
_password_hasher: PasswordHasher = PasswordHasherImpl()
_token_generator: TokenGenerator = TokenGeneratorImpl(
    secret=settings.SECRET_KEY,
    expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional database session.

    Commits on success, rolls back on error.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


SessionDep = Annotated[AsyncSession, Depends(get_session)]


# --- Repos ---


def get_user_repo(session: SessionDep) -> UserRepository:
    """Provide a UserRepository instance."""
    return SqlAlchemyUserRepository(session)


def get_product_repo(session: SessionDep) -> ProductRepository:
    """Provide a ProductRepository instance."""
    return SqlAlchemyProductRepository(session)


def get_cart_repo(session: SessionDep) -> CartRepository:
    """Provide a CartRepository instance."""
    return SqlAlchemyCartRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repo)]
ProductRepoDep = Annotated[ProductRepository, Depends(get_product_repo)]
CartRepoDep = Annotated[CartRepository, Depends(get_cart_repo)]


# --- Auth ---


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_security)],
) -> str:
    """Extract and verify the current user ID from the Bearer token.

    Args:
        credentials: The HTTP Bearer credentials from the Authorization header.

    Returns:
        The authenticated user's ID.

    Raises:
        AuthenticationError: If the token is invalid.
    """
    return _token_generator.verify(credentials.credentials)


CurrentUserId = Annotated[str, Depends(get_current_user_id)]


async def require_admin(
    user_id: CurrentUserId,
    user_repo: UserRepoDep,
) -> str:
    """Verify the current user has admin privileges.

    Args:
        user_id: The current authenticated user's ID.
        user_repo: Repository for user lookup.

    Returns:
        The admin user's ID.

    Raises:
        AuthorizationError: If the user is not an admin.
    """
    user = await user_repo.find_by_id(user_id)
    if not user or user.role != Role.ADMIN:
        raise AuthorizationError("Admin access required")
    return user_id


AdminUserId = Annotated[str, Depends(require_admin)]


# --- Use Cases ---


def get_register_user(user_repo: UserRepoDep) -> RegisterUser:
    """Provide a RegisterUser use case instance."""
    return RegisterUser(user_repo, _password_hasher, _token_generator)


def get_login_user(user_repo: UserRepoDep) -> LoginUser:
    """Provide a LoginUser use case instance."""
    return LoginUser(user_repo, _password_hasher, _token_generator)


def get_list_products(product_repo: ProductRepoDep) -> ListProducts:
    """Provide a ListProducts use case instance."""
    return ListProducts(product_repo)


def get_get_product(product_repo: ProductRepoDep) -> GetProduct:
    """Provide a GetProduct use case instance."""
    return GetProduct(product_repo)


def get_get_cart(cart_repo: CartRepoDep) -> GetCart:
    """Provide a GetCart use case instance."""
    return GetCart(cart_repo)


def get_add_to_cart(cart_repo: CartRepoDep, product_repo: ProductRepoDep) -> AddToCart:
    """Provide an AddToCart use case instance."""
    return AddToCart(cart_repo, product_repo)


def get_remove_from_cart(cart_repo: CartRepoDep) -> RemoveFromCart:
    """Provide a RemoveFromCart use case instance."""
    return RemoveFromCart(cart_repo)


def get_update_cart_item(cart_repo: CartRepoDep) -> UpdateCartItem:
    """Provide an UpdateCartItem use case instance."""
    return UpdateCartItem(cart_repo)


RegisterUserDep = Annotated[RegisterUser, Depends(get_register_user)]
LoginUserDep = Annotated[LoginUser, Depends(get_login_user)]
ListProductsDep = Annotated[ListProducts, Depends(get_list_products)]
GetProductDep = Annotated[GetProduct, Depends(get_get_product)]
GetCartDep = Annotated[GetCart, Depends(get_get_cart)]
AddToCartDep = Annotated[AddToCart, Depends(get_add_to_cart)]
RemoveFromCartDep = Annotated[RemoveFromCart, Depends(get_remove_from_cart)]
UpdateCartItemDep = Annotated[UpdateCartItem, Depends(get_update_cart_item)]
