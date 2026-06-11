"""
=========================================================
Pageless Gradient
OAuth Provider Registry
=========================================================

Responsibilities
----------------
✓ OAuth Client Registry
✓ Google OAuth Registration
✓ GitHub OAuth Registration
✓ Provider Access Helpers
✓ OAuth Configuration Validation

This module should NEVER contain:

✗ Database Logic
✗ User Creation
✗ Session Creation
✗ JWT Logic
✗ Business Logic

=========================================================
"""

from __future__ import annotations

from authlib.integrations.base_client.errors import OAuthError
from authlib.integrations.starlette_client import OAuth

from app.core.config import settings


# =========================================================
# Registry
# =========================================================

oauth = OAuth()


# =========================================================
# Validation
# =========================================================

def validate_google_configuration() -> None:

    if not settings.GOOGLE_CLIENT_ID:
        raise RuntimeError(
            "GOOGLE_CLIENT_ID is not configured."
        )

    if not settings.GOOGLE_CLIENT_SECRET:
        raise RuntimeError(
            "GOOGLE_CLIENT_SECRET is not configured."
        )


def validate_github_configuration() -> None:

    if not settings.GITHUB_CLIENT_ID:
        raise RuntimeError(
            "GITHUB_CLIENT_ID is not configured."
        )

    if not settings.GITHUB_CLIENT_SECRET:
        raise RuntimeError(
            "GITHUB_CLIENT_SECRET is not configured."
        )


# =========================================================
# Google Registration
# =========================================================

if (
    settings.GOOGLE_CLIENT_ID
    and settings.GOOGLE_CLIENT_SECRET
):

    oauth.register(
        name="google",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url=(
            "https://accounts.google.com/"
            ".well-known/openid-configuration"
        ),
        client_kwargs={
            "scope": (
                settings.GOOGLE_DEFAULT_SCOPE
            ),
        },
    )


# =========================================================
# GitHub Registration
# =========================================================

if (
    settings.GITHUB_CLIENT_ID
    and settings.GITHUB_CLIENT_SECRET
):

    oauth.register(
        name="github",
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
        access_token_url=(
            "https://github.com/login/oauth/access_token"
        ),
        authorize_url=(
            "https://github.com/login/oauth/authorize"
        ),
        api_base_url=(
            "https://api.github.com/"
        ),
        client_kwargs={
            "scope": (
                settings.GITHUB_DEFAULT_SCOPE
            ),
        },
    )


# =========================================================
# Provider Access
# =========================================================

def get_google_provider():

    client = oauth.create_client(
        "google"
    )

    if client is None:
        raise RuntimeError(
            "Google OAuth provider "
            "is not registered."
        )

    return client


def get_github_provider():

    client = oauth.create_client(
        "github"
    )

    if client is None:
        raise RuntimeError(
            "GitHub OAuth provider "
            "is not registered."
        )

    return client


# =========================================================
# Global Validation
# =========================================================

def validate_oauth_configuration() -> None:

    if (
        settings.GOOGLE_CLIENT_ID
        or settings.GOOGLE_CLIENT_SECRET
    ):
        validate_google_configuration()

    if (
        settings.GITHUB_CLIENT_ID
        or settings.GITHUB_CLIENT_SECRET
    ):
        validate_github_configuration()


# =========================================================
# Public Exports
# =========================================================

__all__ = [
    "OAuthError",
    "oauth",
    "get_google_provider",
    "get_github_provider",
    "validate_google_configuration",
    "validate_github_configuration",
    "validate_oauth_configuration",
]