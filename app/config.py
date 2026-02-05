from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Attributes:
        DATABASE_URL: PostgreSQL connection string.
        SECRET_KEY: Secret key for JWT signing.
        ACCESS_TOKEN_EXPIRE_MINUTES: Access token lifetime in minutes.
        REFRESH_TOKEN_EXPIRE_DAYS: Refresh token lifetime in days.
        CORS_ORIGINS: Comma-separated list of allowed CORS origins.
        REFRESH_TOKEN_COOKIE_NAME: Name of the refresh token cookie.
        REFRESH_TOKEN_COOKIE_SECURE: Whether cookie requires HTTPS.
    """

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ramona"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    CORS_ORIGINS: str = "http://localhost:4200"

    # Cookie configuration
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    REFRESH_TOKEN_COOKIE_SECURE: bool = False  # Set True in production (HTTPS)

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
