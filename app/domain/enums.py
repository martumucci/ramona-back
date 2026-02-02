"""Domain enumerations for the Ramona Shop."""

from enum import StrEnum


class Role(StrEnum):
    """User roles within the application."""

    CUSTOMER = "customer"
    ADMIN = "admin"


class OrderStatus(StrEnum):
    """Possible states for an order lifecycle."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
