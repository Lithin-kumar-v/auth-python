"""
=========================================================
Pageless Gradient
Enterprise Configuration System
=========================================================

Centralized application configuration.

Features
--------
✓ Environment Management
✓ Database Configuration
✓ Redis Configuration
✓ JWT Configuration
✓ OAuth Configuration
✓ AI Configuration
✓ Cache Configuration
✓ Upload Configuration
✓ Feature Flags
✓ Health Configuration

=========================================================
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):

    # =====================================================
    # Pydantic Settings
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # =====================================================
    # Application
    # =====================================================

    APP_NAME: str = "Pageless Gradient"

    APP_VERSION: str = "1.0.0"

    APP_ENV: Literal[
        "development",
        "staging",
        "production",
    ] = "development"

    DEBUG: bool = True

    API_V1_PREFIX: str = "/api/v1"

    # =====================================================
    # Database
    # =====================================================

    DATABASE_URL: str

    SYNC_DATABASE_URL: str

    DB_POOL_SIZE: int = 10

    DB_MAX_OVERFLOW: int = 20

    DB_POOL_TIMEOUT: int = 30

    DB_POOL_RECYCLE: int = 1800

    # =====================================================
    # Redis
    # =====================================================

    REDIS_URL: str

    REDIS_CACHE_PREFIX: str = "gradient"

    REDIS_DEFAULT_TTL: int = 3600

    # =====================================================
    # JWT
    # =====================================================

    JWT_SECRET: str

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_MINUTES: int = 30

    REFRESH_TOKEN_DAYS: int = 7

    # =====================================================
    # Google OAuth
    # =====================================================

    GOOGLE_CLIENT_ID: str | None = None

    GOOGLE_CLIENT_SECRET: str | None = None

    GOOGLE_REDIRECT_URI: str | None = None

    GOOGLE_DEFAULT_SCOPE: str = (
        "openid email profile"
    )

    # =====================================================
    # GitHub OAuth
    # =====================================================

    GITHUB_CLIENT_ID: str | None = None

    GITHUB_CLIENT_SECRET: str | None = None

    GITHUB_REDIRECT_URI: str | None = None

    GITHUB_DEFAULT_SCOPE: str = (
        "read:user user:email"
    )

    # =====================================================
    # AI
    # =====================================================

    OPENAI_API_KEY: str | None = None

    AI_PROVIDER: str = "openai"

    AI_MODEL: str = "gpt-5"

    # =====================================================
    # Frontend
    # =====================================================

    FRONTEND_URL: str = "http://localhost:5173"

    # =====================================================
    # Authentication
    # =====================================================

    AUTH_COOKIE_NAME: str = "pg_session"

    AUTH_COOKIE_DOMAIN: str | None = None

    AUTH_COOKIE_PATH: str = "/"

    AUTH_COOKIE_HTTPONLY: bool = True

    AUTH_COOKIE_SAMESITE: str = "lax"

    AUTH_COOKIE_MAX_AGE: int = 604800

    SESSION_MAX_AGE_SECONDS: int = 604800

    # =====================================================
    # OAuth Security
    # =====================================================

    OAUTH_STATE_TTL_SECONDS: int = 600

    # =====================================================
    # OAuth Redirects
    # =====================================================

    LOGIN_SUCCESS_REDIRECT: str = "/dashboard"

    LOGIN_FAILURE_REDIRECT: str = "/login"

    # =====================================================
    # Uploads
    # =====================================================

    MAX_FILE_SIZE_MB: int = 50

    MAX_IMAGE_SIZE_MB: int = 20

    MAX_VIDEO_SIZE_MB: int = 500

    # =====================================================
    # Rate Limiting
    # =====================================================

    RATE_LIMIT_ENABLED: bool = True

    RATE_LIMIT_PER_MINUTE: int = 100

    # =====================================================
    # Security
    # =====================================================

    ALLOWED_ORIGINS: str = "*"

    # =====================================================
    # Health
    # =====================================================

    HEALTH_CHECK_TIMEOUT_MS: int = 2000

    READY_OVERALL_TIMEOUT_MS: int = 5000

    # =====================================================
    # Feature Flags
    # =====================================================

    FEATURE_AI_ENABLED: bool = True

    FEATURE_SHARING_ENABLED: bool = True

    FEATURE_ANALYTICS_ENABLED: bool = True

    # =====================================================
    # Computed Fields
    # =====================================================

    @computed_field
    @property
    def IS_PRODUCTION(self) -> bool:
        return self.APP_ENV == "production"

    @computed_field
    @property
    def IS_DEVELOPMENT(self) -> bool:
        return self.APP_ENV == "development"

    @computed_field
    @property
    def IS_STAGING(self) -> bool:
        return self.APP_ENV == "staging"

    @computed_field
    @property
    def COOKIE_SECURE(self) -> bool:
        return self.IS_PRODUCTION

    @computed_field
    @property
    def CORS_ORIGINS(self) -> list[str]:

        if self.ALLOWED_ORIGINS == "*":
            return ["*"]

        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    @computed_field
    @property
    def GOOGLE_CALLBACK_URL(self) -> str | None:
        return self.GOOGLE_REDIRECT_URI

    @computed_field
    @property
    def GITHUB_CALLBACK_URL(self) -> str | None:
        return self.GITHUB_REDIRECT_URI

    # =====================================================
    # Helper Methods
    # =====================================================

    def public_info(self) -> dict[str, str]:
        return {
            "app_name": self.APP_NAME,
            "version": self.APP_VERSION,
            "environment": self.APP_ENV,
        }


# =========================================================
# Singleton Settings
# =========================================================

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()