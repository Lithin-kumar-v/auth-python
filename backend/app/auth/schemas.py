from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


# =========================================================
# Base
# =========================================================

class SchemaBase(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        populate_by_name=True,
    )


# =========================================================
# Register
# =========================================================

class RegisterRequest(
    SchemaBase
):

    email: EmailStr

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# =========================================================
# Login
# =========================================================

class LoginRequest(
    SchemaBase
):

    email: EmailStr

    password: str


# =========================================================
# Google Login
# =========================================================

class GoogleLoginRequest(
    SchemaBase
):

    id_token: str


# =========================================================
# Refresh
# =========================================================

class RefreshTokenRequest(
    SchemaBase
):

    refresh_token: str


# =========================================================
# Logout
# =========================================================

class LogoutRequest(
    SchemaBase
):

    refresh_token: str


# =========================================================
# Password Change
# =========================================================

class ChangePasswordRequest(
    SchemaBase
):

    current_password: str

    new_password: str = Field(
        min_length=8,
        max_length=128,
    )


# =========================================================
# Forgot Password
# =========================================================

class ForgotPasswordRequest(
    SchemaBase
):

    email: EmailStr


# =========================================================
# Reset Password
# =========================================================

class ResetPasswordRequest(
    SchemaBase
):

    token: str

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# =========================================================
# Email Verification
# =========================================================

class VerifyEmailRequest(
    SchemaBase
):

    token: str


class ResendVerificationRequest(
    SchemaBase
):

    email: EmailStr


# =========================================================
# Auth User
# =========================================================

class AuthUser(
    SchemaBase
):

    id: UUID

    email: EmailStr

    username: str

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime

    last_login_at: datetime | None = None


# =========================================================
# Token Pair
# =========================================================

class TokenPairResponse(
    SchemaBase
):

    access_token: str

    refresh_token: str

    token_type: str = "Bearer"


# =========================================================
# Authentication Response
# =========================================================

class AuthResponse(
    TokenPairResponse
):

    user: AuthUser


# =========================================================
# JWT Payload
# =========================================================

class TokenPayload(
    SchemaBase
):

    sub: str

    type: str

    jti: str

    email: str | None = None

    username: str | None = None

    role: str | None = None

    exp: int


# =========================================================
# Session User
# =========================================================

class CurrentUser(
    SchemaBase
):

    id: UUID

    email: EmailStr

    username: str

    is_active: bool

    is_verified: bool


# =========================================================
# Account Status
# =========================================================

class AccountStatusResponse(
    SchemaBase
):

    is_active: bool

    is_verified: bool

    password_set: bool

    google_connected: bool


# =========================================================
# Generic Success
# =========================================================

class MessageResponse(
    SchemaBase
):

    message: str


# =========================================================
# Passwordless Login
# =========================================================

class PasswordlessAccountResponse(
    SchemaBase
):

    error: str = "PASSWORD_NOT_SET"

    message: str = (
        "This account uses OAuth login."
    )