"""Global exception handlers for domain errors."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.errors import (
    AuthenticationError,
    AuthorizationError,
    DomainError,
    NotFoundError,
    ValidationError,
)


async def domain_error_handler(_request: Request, exc: DomainError) -> JSONResponse:
    """Handle generic domain errors as 400 Bad Request."""
    return JSONResponse(status_code=400, content={"detail": exc.message})


async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle not-found errors as 404 Not Found."""
    return JSONResponse(status_code=404, content={"detail": exc.message})


async def authentication_error_handler(
    _request: Request, exc: AuthenticationError
) -> JSONResponse:
    """Handle authentication errors as 401 Unauthorized."""
    return JSONResponse(status_code=401, content={"detail": exc.message})


async def authorization_error_handler(
    _request: Request, exc: AuthorizationError
) -> JSONResponse:
    """Handle authorization errors as 403 Forbidden."""
    return JSONResponse(status_code=403, content={"detail": exc.message})


async def validation_error_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    """Handle validation errors as 422 Unprocessable Entity."""
    return JSONResponse(status_code=422, content={"detail": exc.message})


def register_exception_handlers(app: FastAPI) -> None:
    """Register all domain exception handlers on the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    app.add_exception_handler(NotFoundError, not_found_handler)  # type: ignore[arg-type]
    app.add_exception_handler(AuthenticationError, authentication_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(AuthorizationError, authorization_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(ValidationError, validation_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(DomainError, domain_error_handler)  # type: ignore[arg-type]
