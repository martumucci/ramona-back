"""User domain model."""

from dataclasses import dataclass

from app.domain.enums import Role


@dataclass
class User:
    """Represents a registered user in the system.

    Attributes:
        id: Unique identifier.
        email: User's email address.
        name: Display name.
        hashed_password: Bcrypt-hashed password.
        role: User role (customer or admin).
    """

    id: str
    email: str
    name: str
    hashed_password: str
    role: Role = Role.CUSTOMER
