"""
=========================================================
Pageless Gradient
Enterprise Exception System
=========================================================

Purpose
--------
- Domain Errors
- Business Rule Violations
- Authorization Failures
- Resource Errors
- Validation Failures
- AI Errors
- Infrastructure Errors

=========================================================
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4


# =========================================================
# Base Exception
# =========================================================

class DomainError(Exception):
    """
    Base exception for all application errors.
    """

    status_code = 400

    def __init__(
        self,
        message: str,
        *,
        code: str = "DOMAIN_ERROR",
        details: dict[str, Any] | None = None,
        status_code: int | None = None,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        self.error_id = str(uuid4())

        if status_code:
            self.status_code = status_code

        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": False,
            "error": {
                "id": self.error_id,
                "code": self.code,
                "message": self.message,
                "details": self.details,
            },
        }


# =========================================================
# Authentication
# =========================================================

class UnauthorizedError(DomainError):
    status_code = 401

    def __init__(
        self,
        message: str = "Authentication required",
    ):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
        )


class InvalidCredentialsError(DomainError):
    status_code = 401

    def __init__(
        self,
        message: str = "Invalid credentials",
    ):
        super().__init__(
            message=message,
            code="INVALID_CREDENTIALS",
        )


class TokenExpiredError(DomainError):
    status_code = 401

    def __init__(
        self,
        message: str = "Token expired",
    ):
        super().__init__(
            message=message,
            code="TOKEN_EXPIRED",
        )


class InvalidTokenError(DomainError):
    status_code = 401

    def __init__(
        self,
        message: str = "Invalid token",
    ):
        super().__init__(
            message=message,
            code="INVALID_TOKEN",
        )


class ForbiddenError(DomainError):
    status_code = 403

    def __init__(
        self,
        message: str = "Access denied",
    ):
        super().__init__(
            message=message,
            code="FORBIDDEN",
        )


# =========================================================
# Validation
# =========================================================

class ValidationError(DomainError):
    status_code = 422

    def __init__(
        self,
        message: str = "Validation failed",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            details=details,
        )


class BadRequestError(DomainError):
    status_code = 400

    def __init__(
        self,
        message: str = "Bad request",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            code="BAD_REQUEST",
            details=details,
        )


# =========================================================
# Resources
# =========================================================

class NotFoundError(DomainError):
    status_code = 404

    def __init__(
        self,
        message: str = "Resource not found",
    ):
        super().__init__(
            message=message,
            code="NOT_FOUND",
        )


class AlreadyExistsError(DomainError):
    status_code = 409

    def __init__(
        self,
        message: str = "Resource already exists",
    ):
        super().__init__(
            message=message,
            code="ALREADY_EXISTS",
        )


class ConflictError(DomainError):
    status_code = 409

    def __init__(
        self,
        message: str = "Conflict detected",
    ):
        super().__init__(
            message=message,
            code="CONFLICT",
        )


# =========================================================
# Users
# =========================================================

class UserNotFoundError(NotFoundError):
    def __init__(
        self,
        user_id: str | int | None = None,
    ):
        super().__init__(
            (
                f"User '{user_id}' not found"
                if user_id
                else "User not found"
            )
        )


class UserAlreadyExistsError(AlreadyExistsError):
    def __init__(
        self,
        email: str | None = None,
    ):
        super().__init__(
            (
                f"User already exists with email '{email}'"
                if email
                else "User already exists"
            )
        )


# =========================================================
# Topics
# =========================================================

class TopicNotFoundError(NotFoundError):
    def __init__(
        self,
        topic_id: str | int | None = None,
    ):
        super().__init__(
            (
                f"Topic '{topic_id}' not found"
                if topic_id
                else "Topic not found"
            )
        )


# =========================================================
# Sessions
# =========================================================

class SessionNotFoundError(NotFoundError):
    def __init__(
        self,
        session_id: str | int | None = None,
    ):
        super().__init__(
            (
                f"Session '{session_id}' not found"
                if session_id
                else "Session not found"
            )
        )


# =========================================================
# Blocks
# =========================================================

class BlockNotFoundError(NotFoundError):
    def __init__(
        self,
        block_id: str | int | None = None,
    ):
        super().__init__(
            (
                f"Block '{block_id}' not found"
                if block_id
                else "Block not found"
            )
        )


# =========================================================
# Sharing
# =========================================================

class InvalidShareLinkError(DomainError):
    status_code = 404

    def __init__(
        self,
        message: str = "Invalid share link",
    ):
        super().__init__(
            message=message,
            code="INVALID_SHARE_LINK",
        )


class ShareExpiredError(DomainError):
    status_code = 410

    def __init__(
        self,
        message: str = "Share link expired",
    ):
        super().__init__(
            message=message,
            code="SHARE_EXPIRED",
        )


# =========================================================
# AI
# =========================================================

class AIServiceError(DomainError):
    status_code = 503

    def __init__(
        self,
        message: str = "AI service unavailable",
    ):
        super().__init__(
            message=message,
            code="AI_SERVICE_ERROR",
        )


class AIQuotaExceededError(DomainError):
    status_code = 429

    def __init__(
        self,
        message: str = "AI quota exceeded",
    ):
        super().__init__(
            message=message,
            code="AI_QUOTA_EXCEEDED",
        )


# =========================================================
# Database
# =========================================================

class DatabaseError(DomainError):
    status_code = 500

    def __init__(
        self,
        message: str = "Database error",
    ):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
        )


# =========================================================
# Cache
# =========================================================

class CacheError(DomainError):
    status_code = 500

    def __init__(
        self,
        message: str = "Cache error",
    ):
        super().__init__(
            message=message,
            code="CACHE_ERROR",
        )


# =========================================================
# External Services
# =========================================================

class ExternalServiceError(DomainError):
    status_code = 503

    def __init__(
        self,
        message: str = "External service unavailable",
    ):
        super().__init__(
            message=message,
            code="EXTERNAL_SERVICE_ERROR",
        )


# =========================================================
# Rate Limiting
# =========================================================

class RateLimitExceededError(DomainError):
    status_code = 429

    def __init__(
        self,
        message: str = "Rate limit exceeded",
    ):
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
        )