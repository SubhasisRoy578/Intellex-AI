import json
from typing import Any, List, Union, Optional
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

    # Database Configuration (PostgreSQL)
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "intellex_ai"

    # Generated or explicitly provided URLs
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/intellex_ai"
    ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/intellex_ai"

    # Production Database Pooling Parameters
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

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
    LOG_ROTATION_MAX_BYTES: int = 5242880  # 5 MB
    LOG_ROTATION_BACKUP_COUNT: int = 5

    # Storage and Limits
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10 MB in bytes
    MAX_STORAGE_TARGET_MB: int = 450

    # Clerk Authentication Configuration
    CLERK_SECRET_KEY: str = "sk_test_51ClerkSecretKeyHerePlaceholder"
    CLERK_PUBLISHABLE_KEY: str = "pk_test_51ClerkPublishableKeyHerePlaceholder"
    CLERK_JWT_ISSUER: str = "https://clerk.your-domain.clerk.accounts.dev"

    # AI Conversation Engine Configuration
    AI_PROVIDER: str = "mock"  # "mock", "openai", "gemini"
    OPENAI_API_KEY: Optional[str] = ""
    GEMINI_API_KEY: Optional[str] = ""
    AI_DEFAULT_MODEL: str = "mock-model"
    AI_TIMEOUT_SECONDS: int = 30
    AI_MAX_RETRIES: int = 3

    # Secure Upload Configuration
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"]
    ALLOWED_MIME_TYPES: List[str] = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "image/png",
        "image/jpeg"
    ]

    # Latest Internet Search Configuration
    SEARCH_PROVIDER: str = "mock"  # "mock", "tavily"
    TAVILY_API_KEY: Optional[str] = ""
    SEARCH_DEFAULT_LIMIT: int = 5
    SEARCH_TIMEOUT_SECONDS: int = 15
    SEARCH_MAX_RETRIES: int = 3

    # Configurable Production Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Modular Caching Configuration
    CACHE_BACKEND: str = "in_memory"  # "in_memory", "redis"
    CACHE_DEFAULT_TTL: int = 300


settings = Settings()
