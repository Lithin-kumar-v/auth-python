"""
=========================================================
Pageless Gradient
Security Layer
=========================================================

Features
--------
✓ Password Hashing
✓ Password Verification
✓ Password Strength Validation

✓ JWT Access Tokens
✓ JWT Refresh Tokens

✓ Token Decoding
✓ Token Validation

✓ User Identity Extraction
✓ Token Metadata Helpers

✓ OAuth Ready
✓ Session Ready
✓ Refresh Rotation Ready

=========================================================
"""

from __future__ import annotations

import os

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from typing import Any
from typing import TypedDict

from uuid import uuid4

from dotenv import load_dotenv

from jose import JWTError
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from passlib.context import CryptContext

# =========================================================
# Environment
# =========================================================

load_dotenv()

# =========================================================
# Password Configuration
# =========================================================

PASSWORD_CONTEXT = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)

# =========================================================
# JWT Configuration
# =========================================================

JWT_SECRET = os.getenv("JWT_SECRET")

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256",
)

ACCESS_TOKEN_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_MINUTES",
        "30",
    )
)

REFRESH_TOKEN_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_DAYS",
        "7",
    )
)

JWT_ISSUER = "pageless-gradient"

JWT_AUDIENCE = "pageless-users"

if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET is missing"
    )

# =========================================================
# Token Types
# =========================================================

TOKEN_ACCESS = "access"

TOKEN_REFRESH = "refresh"

# =========================================================
# Payload Typing
# =========================================================

class TokenPayload(
    TypedDict,
    total=False,
):
    sub: str
    email: str | None
    username: str | None
    role: str
    type: str
    jti: str
    iss: str
    aud: str

# =========================================================
# Helpers
# =========================================================

def utc_now() -> datetime:

    return datetime.now(
        timezone.utc
    )

# =========================================================
# Password Validation
# =========================================================

def validate_password_strength(
    password: str,
) -> bool:

    if not password:
        return False

    if len(password) < 8:
        return False

    has_upper = any(
        c.isupper()
        for c in password
    )

    has_lower = any(
        c.islower()
        for c in password
    )

    has_digit = any(
        c.isdigit()
        for c in password
    )

    return all(
        [
            has_upper,
            has_lower,
            has_digit,
        ]
    )

# =========================================================
# Password Hashing
# =========================================================

def hash_password(
    password: str,
) -> str:

    return PASSWORD_CONTEXT.hash(
        password
    )

def verify_password(
    plain_password: str,
    hashed_password: str | None,
) -> bool:

    if not hashed_password:
        return False

    try:

        return PASSWORD_CONTEXT.verify(
            plain_password,
            hashed_password,
        )

    except Exception:

        return False

# =========================================================
# Internal Token Builder
# =========================================================

def _create_token(
    *,
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra: dict[str, Any] | None = None,
) -> str:

    now = utc_now()

    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "jti": str(uuid4()),
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + expires_delta,
    }

    if extra:
        payload.update(extra)

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

# =========================================================
# Access Token
# =========================================================

def create_access_token(
    *,
    user_id: str,
    email: str | None = None,
    username: str | None = None,
    role: str = "member",
) -> str:

    return _create_token(
        subject=user_id,
        token_type=TOKEN_ACCESS,
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_MINUTES
        ),
        extra={
            "email": email,
            "username": username,
            "role": role,
        },
    )

# =========================================================
# Refresh Token
# =========================================================

def create_refresh_token(
    *,
    user_id: str,
) -> str:

    return _create_token(
        subject=user_id,
        token_type=TOKEN_REFRESH,
        expires_delta=timedelta(
            days=REFRESH_TOKEN_DAYS
        ),
    )

# =========================================================
# Token Pair
# =========================================================

def create_token_pair(
    *,
    user_id: str,
    email: str | None = None,
    username: str | None = None,
    role: str = "member",
) -> dict[str, str]:

    return {
        "access_token": create_access_token(
            user_id=user_id,
            email=email,
            username=username,
            role=role,
        ),
        "refresh_token": create_refresh_token(
            user_id=user_id,
        ),
        "token_type": "Bearer",
    }

# =========================================================
# Decode
# =========================================================

def decode_token(
    token: str,
) -> dict[str, Any]:

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[
                JWT_ALGORITHM,
            ],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )

        return payload

    except ExpiredSignatureError:

        raise ValueError(
            "Token expired"
        )

    except JWTError:

        raise ValueError(
            "Invalid token"
        )

# =========================================================
# Validation
# =========================================================

def validate_access_token(
    token: str,
) -> dict[str, Any]:

    payload = decode_token(
        token
    )

    if payload.get(
        "type"
    ) != TOKEN_ACCESS:

        raise ValueError(
            "Invalid access token"
        )

    return payload

def validate_refresh_token(
    token: str,
) -> dict[str, Any]:

    payload = decode_token(
        token
    )

    if payload.get(
        "type"
    ) != TOKEN_REFRESH:

        raise ValueError(
            "Invalid refresh token"
        )

    return payload

# =========================================================
# Token Helpers
# =========================================================

def get_refresh_expiry() -> datetime:
    return utc_now() + timedelta(
        days=REFRESH_TOKEN_DAYS
    )

def is_access_token(
    payload: dict[str, Any],
) -> bool:

    return (
        payload.get("type")
        == TOKEN_ACCESS
    )

def is_refresh_token(
    payload: dict[str, Any],
) -> bool:

    return (
        payload.get("type")
        == TOKEN_REFRESH
    )

# =========================================================
# User Helpers
# =========================================================

def get_user_id(
    token: str,
) -> str:

    payload = validate_access_token(
        token
    )

    return str(
        payload["sub"]
    )

def get_user_role(
    token: str,
) -> str:

    payload = validate_access_token(
        token
    )

    return str(
        payload.get(
            "role",
            "member",
        )
    )


def get_user_email(
    token: str,
) -> str | None:

    payload = validate_access_token(
        token
    )

    return payload.get(
        "email"
    )


def get_username(
    token: str,
) -> str | None:

    payload = validate_access_token(
        token
    )

    return payload.get(
        "username"
    )


def token_is_expired(
    token: str,
) -> bool:

    try:

        decode_token(
            token
        )

        return False

    except ValueError:

        return True
    
# =========================================================
# Metadata Helpers
# =========================================================

def get_token_id(
    token: str,
) -> str:

    payload = decode_token(
        token
    )

    return str(
        payload["jti"]
    )

def get_token_type(
    token: str,
) -> str:

    payload = decode_token(
        token
    )

    return str(
        payload["type"]
    )

# =========================================================
# Authorization Header
# =========================================================

def extract_bearer_token(
    authorization: str,
) -> str:

    if not authorization:

        raise ValueError(
            "Missing authorization header"
        )

    parts = authorization.split()

    if len(parts) != 2:

        raise ValueError(
            "Invalid authorization header"
        )

    scheme, token = parts

    if scheme.lower() != "bearer":

        raise ValueError(
            "Invalid authorization scheme"
        )

    return token