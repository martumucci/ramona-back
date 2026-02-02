"""Use case for registering a new user."""

import uuid
from dataclasses import dataclass

from app.application.dtos import AuthResult
from app.application.interfaces.password_hasher import PasswordHasher
from app.application.interfaces.token_generator import TokenGenerator
from app.application.interfaces.user_repository import UserRepository
from app.domain.errors import ValidationError
from app.domain.models.user import User


@dataclass
class RegisterUserInput:
    """Input data for user registration.

    Attributes:
        email: The user's email address.
        name: The user's display name.
        password: The plain-text password.
    """

    email: str
    name: str
    password: str


class RegisterUser:
    """Registers a new user account and returns an access token.

    Args:
        user_repo: Repository for user persistence.
        password_hasher: Service for hashing passwords.
        token_generator: Service for creating JWT tokens.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator,
    ) -> None:
        self._user_repo = user_repo
        self._hasher = password_hasher
        self._token_gen = token_generator

    async def execute(self, input_data: RegisterUserInput) -> AuthResult:
        """Execute the registration use case.

        Args:
            input_data: Registration details.

        Returns:
            An AuthResult with the access token and user info.

        Raises:
            ValidationError: If the email is already registered.
        """
        existing = await self._user_repo.find_by_email(input_data.email)
        if existing:
            raise ValidationError("Email already registered")

        user = User(
            id=str(uuid.uuid4()),
            email=input_data.email,
            name=input_data.name,
            hashed_password=self._hasher.hash(input_data.password),
        )
        await self._user_repo.save(user)

        token = self._token_gen.generate(user.id)
        return AuthResult(
            access_token=token,
            token_type="bearer",
            user_id=user.id,
            name=user.name,
        )
