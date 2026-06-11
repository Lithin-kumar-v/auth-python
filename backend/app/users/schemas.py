from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


# =========================================================
# Base Config
# =========================================================

class SchemaBase(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


# =========================================================
# User Profile
# =========================================================

class UserProfileBase(
    SchemaBase
):

    display_name: str | None = Field(
        default=None,
        max_length=120,
    )

    avatar_url: str | None = Field(
        default=None,
        max_length=1000,
    )

    bio: str | None = Field(
        default=None,
        max_length=500,
    )

    timezone: str = Field(
        default="UTC",
        max_length=100,
    )

    language: str = Field(
        default="en",
        max_length=20,
    )


class UserProfileCreate(
    UserProfileBase
):

    pass


class UserProfileUpdate(
    SchemaBase
):

    display_name: str | None = Field(
        default=None,
        max_length=120,
    )

    avatar_url: str | None = Field(
        default=None,
        max_length=1000,
    )

    bio: str | None = Field(
        default=None,
        max_length=500,
    )

    timezone: str | None = None

    language: str | None = None


class UserProfileResponse(
    UserProfileBase
):

    id: UUID

    user_id: UUID

    created_at: datetime

    updated_at: datetime


# =========================================================
# User Base
# =========================================================

class UserBase(
    SchemaBase
):

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=50,
    )


# =========================================================
# Registration
# =========================================================

class UserCreate(
    UserBase
):

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# =========================================================
# Login
# =========================================================

class UserLogin(
    SchemaBase
):

    email: EmailStr

    password: str


# =========================================================
# User Update
# =========================================================

class UserUpdate(
    SchemaBase
):

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )

class AdminUserUpdate(
    SchemaBase
):

    is_active: bool | None = None

    is_verified: bool | None = None

# =========================================================
# User Response
# =========================================================

class UserResponse(
    UserBase
):

    id: UUID

    auth_provider: str

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime

    last_login_at: datetime | None


# =========================================================
# User Detail
# Explicit Join Result
# =========================================================

class UserDetailResponse(
    UserResponse
):

    profile: UserProfileResponse | None = None


# =========================================================
# Internal User
# =========================================================

class UserInDB(
    UserResponse
):

    password_hash: str | None


# =========================================================
# Auth
# =========================================================

class TokenPairResponse(
    SchemaBase
):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"


class AuthResponse(
    SchemaBase
):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"

    user: UserResponse


# =========================================================
# Current User
# =========================================================

class CurrentUser(
    UserResponse
):

    pass


# =========================================================
# Public User
# =========================================================

class PublicUserResponse(
    SchemaBase
):

    id: UUID

    username: str


# =========================================================
# User Summary
# =========================================================

class UserSummaryResponse(
    SchemaBase
):

    id: UUID

    email: EmailStr

    username: str

    is_active: bool

    is_verified: bool

    created_at: datetime


# =========================================================
# Password
# =========================================================

class ChangePasswordRequest(
    SchemaBase
):

    current_password: str

    new_password: str = Field(
        min_length=8,
        max_length=128,
    )


class ResetPasswordRequest(
    SchemaBase
):

    token: str

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# =========================================================
# Verification
# =========================================================

class VerifyEmailRequest(
    SchemaBase
):

    token: str


class ResendVerificationRequest(
    SchemaBase
):

    email: EmailStr