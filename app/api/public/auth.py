"""Authentication route handlers.

Provides endpoints for user registration, login, token refresh, and logout.
Uses JWT tokens with HttpOnly cookies for refresh token storage.
"""

from typing import Annotated

from fastapi import APIRouter, Cookie, Response

from app.api.dependencies import LoginUserDep, RegisterUserDep, TokenGeneratorDep
from app.api.schemas import AuthResponse, LoginRequest, RegisterRequest
from app.application.use_cases.auth.login_user import LoginUserInput
from app.application.use_cases.auth.register_user import RegisterUserInput
from app.config import settings
from app.domain.errors import AuthenticationError

router = APIRouter(prefix="/auth", tags=["auth"])

# Type alias for the refresh token cookie parameter
RefreshTokenCookie = Annotated[
    str | None,
    Cookie(alias=settings.REFRESH_TOKEN_COOKIE_NAME),
]


def _set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Set the HttpOnly cookie containing the refresh token.

    Args:
        response: FastAPI response object to set the cookie on.
        refresh_token: The JWT refresh token to store.
    """
    max_age_seconds = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite="lax",
        max_age=max_age_seconds,
        path="/api/auth",
    )


def _delete_refresh_cookie(response: Response) -> None:
    """Delete the refresh token cookie.

    Args:
        response: FastAPI response object to delete the cookie from.
    """
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        path="/api/auth",
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    body: RegisterRequest,
    use_case: RegisterUserDep,
    token_generator: TokenGeneratorDep,
    response: Response,
) -> AuthResponse:
    """Register a new user account.

    Args:
        body: Registration data (email, name, password).
        use_case: Injected registration use case.
        token_generator: Injected token generator.
        response: FastAPI response for setting cookies.

    Returns:
        AuthResponse with access token and user info.
    """
    result = await use_case.execute(
        RegisterUserInput(
            email=body.email,
            name=body.name,
            password=body.password,
        )
    )

    refresh_token = token_generator.generate_refresh_token(result.user_id)
    _set_refresh_cookie(response, refresh_token)

    return AuthResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        user_id=result.user_id,
        name=result.name,
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    body: LoginRequest,
    use_case: LoginUserDep,
    token_generator: TokenGeneratorDep,
    response: Response,
) -> AuthResponse:
    """Authenticate an existing user.

    Args:
        body: Login credentials (email, password).
        use_case: Injected login use case.
        token_generator: Injected token generator.
        response: FastAPI response for setting cookies.

    Returns:
        AuthResponse with access token and user info.
    """
    result = await use_case.execute(
        LoginUserInput(
            email=body.email,
            password=body.password,
        )
    )

    refresh_token = token_generator.generate_refresh_token(result.user_id)
    _set_refresh_cookie(response, refresh_token)

    return AuthResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        user_id=result.user_id,
        name=result.name,
    )


@router.post("/refresh")
async def refresh(
    token_generator: TokenGeneratorDep,
    response: Response,
    refresh_token: RefreshTokenCookie = None,
) -> dict[str, str]:
    """Get a new access token using the refresh token cookie.

    Args:
        token_generator: Injected token generator.
        response: FastAPI response for rotating the cookie.
        refresh_token: Refresh token from HttpOnly cookie.

    Returns:
        Dict with new access_token and token_type.

    Raises:
        AuthenticationError: If no refresh token or token is invalid.
    """
    if not refresh_token:
        raise AuthenticationError("No refresh token provided")

    # Verify refresh token and extract user_id
    user_id = token_generator.verify(refresh_token, expected_type="refresh")

    # Generate new access token
    new_access_token = token_generator.generate(user_id)

    # Rotate refresh token (security best practice)
    new_refresh_token = token_generator.generate_refresh_token(user_id)
    _set_refresh_cookie(response, new_refresh_token)

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    """Log out by deleting the refresh token cookie.

    Args:
        response: FastAPI response for deleting the cookie.

    Returns:
        Confirmation message.
    """
    _delete_refresh_cookie(response)
    return {"message": "Logged out successfully"}
