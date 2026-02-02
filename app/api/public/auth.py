"""Authentication route handlers."""

from fastapi import APIRouter

from app.api.dependencies import LoginUserDep, RegisterUserDep
from app.api.schemas import AuthResponse, LoginRequest, RegisterRequest
from app.application.use_cases.auth.login_user import LoginUserInput
from app.application.use_cases.auth.register_user import RegisterUserInput

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(body: RegisterRequest, use_case: RegisterUserDep) -> AuthResponse:
    """Register a new user account."""
    result = await use_case.execute(RegisterUserInput(
        email=body.email,
        name=body.name,
        password=body.password,
    ))
    return AuthResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        user_id=result.user_id,
        name=result.name,
    )


@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, use_case: LoginUserDep) -> AuthResponse:
    """Authenticate an existing user."""
    result = await use_case.execute(LoginUserInput(
        email=body.email,
        password=body.password,
    ))
    return AuthResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        user_id=result.user_id,
        name=result.name,
    )
