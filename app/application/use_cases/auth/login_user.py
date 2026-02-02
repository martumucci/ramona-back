"""Use case for authenticating an existing user."""

from dataclasses import dataclass

from app.application.dtos import AuthResult
from app.application.interfaces.password_hasher import PasswordHasher
from app.application.interfaces.token_generator import TokenGenerator
from app.application.interfaces.user_repository import UserRepository
from app.domain.errors import AuthenticationError


@dataclass
class LoginUserInput:
    """Input data for user login.

    Attributes:
        email: The user's email address.
        password: The plain-text password.
    """

    email: str
    password: str


class LoginUser:
    """Authenticates a user and returns an access token.

    Args:
        user_repo: Repository for user persistence.
        password_hasher: Service for verifying passwords.
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

    async def execute(self, input_data: LoginUserInput) -> AuthResult:
        """Execute the login use case.

        Args:
            input_data: Login credentials.

        Returns:
            An AuthResult with the access token and user info.

        Raises:
            AuthenticationError: If the credentials are invalid.
        """
        user = await self._user_repo.find_by_email(input_data.email)
        if not user:
            raise AuthenticationError("Invalid credentials")

        if not self._hasher.verify(input_data.password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")

        token = self._token_gen.generate(user.id)
        return AuthResult(
            access_token=token,
            token_type="bearer",
            user_id=user.id,
            name=user.name,
        )
