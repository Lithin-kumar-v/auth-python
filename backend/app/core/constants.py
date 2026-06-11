"""
=========================================================
Pageless Gradient
Application Constants
=========================================================

Centralized constants used across:

- Auth
- Users
- Topics
- Sessions
- Blocks
- Sharing
- AI
- Analytics

=========================================================
"""

from __future__ import annotations

# =========================================================
# Application
# =========================================================

APP_NAME = "Pageless Gradient"

APP_SLUG = "gradient"

APP_COMPANY = "Pageless"

APP_VERSION = "1.0.0"

API_VERSION = "v1"

# =========================================================
# Pagination
# =========================================================

DEFAULT_PAGE = 1

DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100

MAX_SEARCH_LENGTH = 200

# =========================================================
# Cache
# =========================================================

CACHE_NAMESPACE = "gradient"

DEFAULT_CACHE_TTL = 3600

SHORT_CACHE_TTL = 300

LONG_CACHE_TTL = 86400

# =========================================================
# Authentication
# =========================================================

TOKEN_TYPE_BEARER = "Bearer"

ACCESS_TOKEN_MINUTES = 30

REFRESH_TOKEN_DAYS = 7

PASSWORD_MIN_LENGTH = 8

PASSWORD_MAX_LENGTH = 128

# =========================================================
# User Roles
# =========================================================

ROLE_OWNER = "owner"

ROLE_ADMIN = "admin"

ROLE_EDITOR = "editor"

ROLE_MEMBER = "member"

ROLE_VIEWER = "viewer"

USER_ROLES = [
    ROLE_OWNER,
    ROLE_ADMIN,
    ROLE_EDITOR,
    ROLE_MEMBER,
    ROLE_VIEWER,
]

# =========================================================
# User Status
# =========================================================

STATUS_ACTIVE = "active"

STATUS_INACTIVE = "inactive"

STATUS_SUSPENDED = "suspended"

STATUS_PENDING = "pending"

USER_STATUSES = [
    STATUS_ACTIVE,
    STATUS_INACTIVE,
    STATUS_SUSPENDED,
    STATUS_PENDING,
]

# =========================================================
# Topic Visibility
# =========================================================

VISIBILITY_PRIVATE = "private"

VISIBILITY_PUBLIC = "public"

VISIBILITY_UNLISTED = "unlisted"

VISIBILITY_TEAM = "team"

VISIBILITY_OPTIONS = [
    VISIBILITY_PRIVATE,
    VISIBILITY_PUBLIC,
    VISIBILITY_UNLISTED,
    VISIBILITY_TEAM,
]

# =========================================================
# Sessions
# =========================================================

SESSION_DRAFT = "draft"

SESSION_ACTIVE = "active"

SESSION_ARCHIVED = "archived"

SESSION_COMPLETED = "completed"

SESSION_STATUSES = [
    SESSION_DRAFT,
    SESSION_ACTIVE,
    SESSION_ARCHIVED,
    SESSION_COMPLETED,
]

# =========================================================
# Blocks
# =========================================================

BLOCK_TEXT = "text"

BLOCK_CODE = "code"

BLOCK_RESOURCE = "resource"

BLOCK_IMAGE = "image"

BLOCK_VIDEO = "video"

BLOCK_AUDIO = "audio"

BLOCK_FILE = "file"

BLOCK_MARKDOWN = "markdown"

BLOCK_AI = "ai"

BLOCK_TYPES = [
    BLOCK_TEXT,
    BLOCK_CODE,
    BLOCK_RESOURCE,
    BLOCK_IMAGE,
    BLOCK_VIDEO,
    BLOCK_AUDIO,
    BLOCK_FILE,
    BLOCK_MARKDOWN,
    BLOCK_AI,
]

# =========================================================
# Resource Types
# =========================================================

RESOURCE_LINK = "link"

RESOURCE_DOCUMENT = "document"

RESOURCE_VIDEO = "video"

RESOURCE_IMAGE = "image"

RESOURCE_AUDIO = "audio"

RESOURCE_TYPES = [
    RESOURCE_LINK,
    RESOURCE_DOCUMENT,
    RESOURCE_VIDEO,
    RESOURCE_IMAGE,
    RESOURCE_AUDIO,
]

# =========================================================
# Sharing
# =========================================================

SHARE_PUBLIC = "public"

SHARE_PRIVATE = "private"

SHARE_PASSWORD = "password"

SHARE_TYPES = [
    SHARE_PUBLIC,
    SHARE_PRIVATE,
    SHARE_PASSWORD,
]

DEFAULT_SHARE_EXPIRY_DAYS = 30

# =========================================================
# AI
# =========================================================

AI_PROVIDER_OPENAI = "openai"

AI_PROVIDER_ANTHROPIC = "anthropic"

AI_PROVIDER_GEMINI = "gemini"

AI_PROVIDERS = [
    AI_PROVIDER_OPENAI,
    AI_PROVIDER_ANTHROPIC,
    AI_PROVIDER_GEMINI,
]

AI_MAX_PROMPT_LENGTH = 100000

AI_MAX_RESPONSE_LENGTH = 50000

# =========================================================
# Uploads
# =========================================================

MAX_FILE_SIZE_MB = 50

MAX_IMAGE_SIZE_MB = 20

MAX_VIDEO_SIZE_MB = 500

ALLOWED_IMAGE_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/gif",
]

ALLOWED_DOCUMENT_TYPES = [
    "application/pdf",
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]

# =========================================================
# Analytics
# =========================================================

ANALYTICS_DAILY = "daily"

ANALYTICS_WEEKLY = "weekly"

ANALYTICS_MONTHLY = "monthly"

# =========================================================
# Health
# =========================================================

HEALTHY = "healthy"

UNHEALTHY = "unhealthy"

DEGRADED = "degraded"

# =========================================================
# Error Codes
# =========================================================

ERROR_VALIDATION = "VALIDATION_ERROR"

ERROR_UNAUTHORIZED = "UNAUTHORIZED"

ERROR_FORBIDDEN = "FORBIDDEN"

ERROR_NOT_FOUND = "NOT_FOUND"

ERROR_CONFLICT = "CONFLICT"

ERROR_INTERNAL = "INTERNAL_ERROR"

# =========================================================
# Database
# =========================================================

DEFAULT_DB_POOL_SIZE = 10

DEFAULT_DB_MAX_OVERFLOW = 20

# =========================================================
# Redis
# =========================================================

REDIS_LOCK_PREFIX = "lock"

REDIS_SESSION_PREFIX = "session"

REDIS_RATE_LIMIT_PREFIX = "rate_limit"

REDIS_CACHE_PREFIX = "cache"

# =========================================================
# Rate Limiting
# =========================================================

RATE_LIMIT_LOGIN = 5

RATE_LIMIT_REGISTER = 5

RATE_LIMIT_API = 100

RATE_LIMIT_WINDOW_SECONDS = 60