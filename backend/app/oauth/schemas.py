"""
=========================================================
Pageless Gradient
OAuth Schemas
=========================================================

Responsibilities
----------------
✓ Provider User Data
✓ OAuth Provider Payloads
✓ OAuth Login Responses
✓ OAuth Callback Responses
✓ OAuth Account Linking
✓ OAuth Error Responses

This module should NEVER contain:

✗ Database Models
✗ Business Logic
✗ JWT Logic
✗ Session Logic

=========================================================
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


# =========================================================
# Base Config
# =========================================================

class OAuthBaseSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

# =========================================================
# Password Setup
# =========================================================

class PasswordSetupRequest(
    OAuthBaseSchema
):

    password: str

# =========================================================
# Provider User
# =========================================================

class OAuthProviderUser(OAuthBaseSchema):

    provider_id: str = Field(
        ...,
        description="OAuth provider user id",
    )

    email: EmailStr

    username: str

    display_name: str | None = None

    avatar_url: str | None = None

    provider: str

    verified_email: bool = True


# =========================================================
# Google User Info
# =========================================================

class GoogleUserInfo(OAuthBaseSchema):

    sub: str

    email: EmailStr

    email_verified: bool = True

    name: str | None = None

    picture: str | None = None

    given_name: str | None = None

    family_name: str | None = None

    locale: str | None = None


# =========================================================
# GitHub User Info
# =========================================================

class GitHubUserInfo(OAuthBaseSchema):

    id: int

    login: str

    name: str | None = None

    avatar_url: str | None = None

    email: EmailStr | None = None


# =========================================================
# OAuth Account
# =========================================================

class OAuthAccountInfo(OAuthBaseSchema):

    provider: str

    provider_id: str

    linked: bool

    linked_at: datetime | None = None


# =========================================================
# OAuth Login Response
# =========================================================

class OAuthLoginResponse(
    OAuthBaseSchema
):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"

    expires_in: int | None = None

    user: dict

# =========================================================
# OAuth Callback Response
# =========================================================

class OAuthCallbackResponse(
    OAuthBaseSchema
):

    success: bool = True

    provider: str

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"

    expires_in: int | None = None

    user: dict


# =========================================================
# OAuth Link Response
# =========================================================

class OAuthLinkResponse(OAuthBaseSchema):

    success: bool = True

    provider: str

    message: str


# =========================================================
# OAuth Unlink Response
# =========================================================

class OAuthUnlinkResponse(OAuthBaseSchema):

    success: bool = True

    provider: str

    message: str


# =========================================================
# OAuth Error Response
# =========================================================

class OAuthErrorResponse(OAuthBaseSchema):

    success: bool = False

    error: str

    detail: str | None = None

    provider: str | None = None


# =========================================================
# OAuth State Payload
# =========================================================

class OAuthStatePayload(OAuthBaseSchema):

    provider: str

    redirect_uri: str | None = None


# =========================================================
# OAuth Providers
# =========================================================

class OAuthProvidersResponse(OAuthBaseSchema):

    google_enabled: bool

    github_enabled: bool


# =========================================================
# Public Exports
# =========================================================

__all__ = [
    "OAuthProviderUser",
    "GoogleUserInfo",
    "GitHubUserInfo",
    "OAuthAccountInfo",
    "OAuthLoginResponse",
    "OAuthCallbackResponse",
    "OAuthLinkResponse",
    "OAuthUnlinkResponse",
    "OAuthErrorResponse",
    "OAuthStatePayload",
    "OAuthProvidersResponse",
    "PasswordSetupRequest",
]