"""Interface for user persistence operations."""

from abc import ABC, abstractmethod

from app.domain.models.user import User


class UserRepository(ABC):
    """Abstract repository for user data access."""

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        """Find a user by email address.

        Args:
            email: The user's email.

        Returns:
            The User if found, None otherwise.
        """
        ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None:
        """Find a user by unique identifier.

        Args:
            user_id: The user's UUID string.

        Returns:
            The User if found, None otherwise.
        """
        ...

    @abstractmethod
    async def save(self, user: User) -> User:
        """Persist a user (insert or update).

        Args:
            user: The user domain object to save.

        Returns:
            The saved user.
        """
        ...
