import json
from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # App Settings
    APP_NAME: str = "Intellex AI"
    APP_ENV: str = "production"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "super-secret-key-change-in-production-1234567890"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "intellex_ai"

    # Generated or explicitly provided URLs
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/intellex_ai"
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/intellex_ai"

    # CORS configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], Any]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            try:
                return json.loads(v)
            except Exception:
                raise ValueError(f"Invalid CORS JSON array: {v}")
        return v

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "JSON"  # JSON or CONSOLE

    # Storage and Limits
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10 MB in bytes
    MAX_STORAGE_TARGET_MB: int = 450

    # Clerk Authentication Configuration
    CLERK_SECRET_KEY: str = "sk_test_51ClerkSecretKeyHerePlaceholder"
    CLERK_PUBLISHABLE_KEY: str = "pk_test_51ClerkPublishableKeyHerePlaceholder"
    CLERK_JWT_ISSUER: str = "https://clerk.your-domain.clerk.accounts.dev"


settings = Settings()
