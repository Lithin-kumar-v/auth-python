from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# =========================================================
# Base
# =========================================================

class SchemaBase(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


# =========================================================
# Session Base
# =========================================================

class SessionBase(
    SchemaBase
):

    session_name: str | None = Field(
        default=None,
        max_length=255,
    )

    login_method: str

    device_name: str | None = None

    device_type: str | None = None

    browser: str | None = None

    browser_version: str | None = None

    os: str | None = None

    os_version: str | None = None

    country: str | None = None

    region: str | None = None

    city: str | None = None

    timezone: str | None = None


# =========================================================
# Internal Create
# =========================================================

class SessionCreate(
    SessionBase
):

    user_id: UUID

    refresh_token_hash: str

    token_family: str | None = None

    replaced_by_token: str | None = None

    user_agent: str | None = None

    ip_address: str | None = None

    expires_at: datetime


# =========================================================
# Internal Update
# =========================================================

class SessionUpdate(
    SchemaBase
):

    last_activity: datetime | None = None

    revoked: bool | None = None

    revoked_reason: str | None = None

    revoked_at: datetime | None = None

    suspicious: bool | None = None

    replaced_by_token: str | None = None


# =========================================================
# Public Session
# =========================================================

class SessionResponse(
    SessionBase
):

    id: UUID

    user_id: UUID

    login_at: datetime

    last_activity: datetime

    expires_at: datetime

    is_current: bool

    revoked: bool

    suspicious: bool

    created_at: datetime

    updated_at: datetime


# =========================================================
# Device List Item
# =========================================================

class SessionDeviceResponse(
    SchemaBase
):

    id: UUID

    session_name: str | None

    device_name: str | None

    device_type: str | None

    browser: str | None

    os: str | None

    country: str | None

    city: str | None

    login_at: datetime

    last_activity: datetime

    expires_at: datetime

    is_current: bool

    revoked: bool


# =========================================================
# Session Detail
# =========================================================

class SessionDetailResponse(
    SessionResponse
):

    token_family: str | None

    user_agent: str | None

    ip_address: str | None

    revoked_reason: str | None

    revoked_at: datetime | None


# =========================================================
# Logout Device
# =========================================================

class LogoutSessionRequest(
    SchemaBase
):

    session_id: UUID


# =========================================================
# Logout All
# =========================================================

class LogoutAllSessionsResponse(
    SchemaBase
):

    success: bool

    revoked_sessions: int


# =========================================================
# Refresh Token Rotation
# =========================================================

class RefreshSessionRequest(
    SchemaBase
):

    refresh_token: str


class RefreshSessionResponse(
    SchemaBase
):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"


# =========================================================
# Session Statistics
# =========================================================

class SessionStatsResponse(
    SchemaBase
):

    total_sessions: int

    active_sessions: int

    revoked_sessions: int

    suspicious_sessions: int


# =========================================================
# Admin Session View
# =========================================================

class AdminSessionResponse(
    SessionResponse
):

    refresh_token_hash: str

    ip_address: str | None

    user_agent: str | None


# =========================================================
# Current Session
# =========================================================

class CurrentSessionResponse(
    SessionDeviceResponse
):

    pass