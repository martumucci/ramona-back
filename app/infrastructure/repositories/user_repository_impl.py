"""SQLAlchemy implementation of the UserRepository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.user_repository import UserRepository
from app.domain.enums import Role
from app.domain.models.user import User
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.utils import parse_uuid


class SqlAlchemyUserRepository(UserRepository):
    """Persists User domain objects using SQLAlchemy.

    Args:
        session: An async SQLAlchemy session.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_email(self, email: str) -> User | None:
        """Find a user by email address.

        Args:
            email: The user's email.

        Returns:
            The User if found, None otherwise.
        """
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def find_by_id(self, user_id: str) -> User | None:
        """Find a user by unique identifier.

        Args:
            user_id: The user's UUID string.

        Returns:
            The User if found, None otherwise.
        """
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == parse_uuid(user_id))
        )
        row = result.scalar_one_or_none()
        return self._to_domain(row) if row else None

    async def save(self, user: User) -> User:
        """Persist a user (insert or update).

        Args:
            user: The user domain object to save.

        Returns:
            The saved user.
        """
        model = UserModel(
            id=parse_uuid(user.id),
            email=user.email,
            name=user.name,
            hashed_password=user.hashed_password,
            role=user.role.value,
        )
        self._session.add(model)
        await self._session.flush()
        return user

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=str(model.id),
            email=model.email,
            name=model.name,
            hashed_password=model.hashed_password,
            role=Role(model.role),
        )
