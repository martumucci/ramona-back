"""Domain exceptions for the Ramona Shop."""


class DomainError(Exception):
    """Base exception for all domain-level errors."""

    def __init__(self, message: str = "Domain error") -> None:
        self.message = message
        super().__init__(self.message)


class NotFoundError(DomainError):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message)


class AuthenticationError(DomainError):
    """Raised when authentication credentials are invalid."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message)


class AuthorizationError(DomainError):
    """Raised when a user lacks permission for the requested action."""

    def __init__(self, message: str = "Not authorized") -> None:
        super().__init__(message)


class ValidationError(DomainError):
    """Raised when input data fails domain validation rules."""

    def __init__(self, message: str = "Validation error") -> None:
        super().__init__(message)
