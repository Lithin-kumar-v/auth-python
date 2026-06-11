from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from db import get_redis

from app.core.config import settings

from app.core.security import (
    extract_bearer_token,
    validate_access_token,
)

from app.users.repository import UserRepository


# =========================================================
# Database
# =========================================================

async def get_database(
    db: AsyncSession = Depends(
        get_async_session
    ),
) -> AsyncSession:

    return db


DatabaseDep = Annotated[
    AsyncSession,
    Depends(get_database),
]

# =========================================================
# Redis
# =========================================================

async def get_cache():

    cache = await get_redis()

    if cache is None:

        raise HTTPException(
            status_code=503,
            detail="Redis unavailable",
        )

    return cache


CacheDep = Annotated[
    object,
    Depends(get_cache),
]

# =========================================================
# Settings
# =========================================================

def get_settings():

    return settings


SettingsDep = Annotated[
    object,
    Depends(get_settings),
]

# =========================================================
# Request Context
# =========================================================

async def get_request_context(
    request: Request,
):

    return {
        "ip": (
            request.client.host
            if request.client
            else None
        ),
        "path": request.url.path,
        "method": request.method,
        "user_agent": request.headers.get(
            "user-agent"
        ),
    }


RequestContextDep = Annotated[
    dict,
    Depends(get_request_context),
]

# =========================================================
# Authorization Header
# =========================================================

async def get_authorization_header(
    authorization: str | None = Header(
        default=None,
    ),
) -> str:

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Authorization header missing",
        )

    return authorization


AuthorizationDep = Annotated[
    str,
    Depends(
        get_authorization_header
    ),
]

# =========================================================
# Current User
# =========================================================

async def get_current_user(
    authorization: AuthorizationDep,
    db: DatabaseDep,
):

    try:

        token = extract_bearer_token(
            authorization
        )

        payload = validate_access_token(
            token
        )

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid token payload",
        )

    repo = UserRepository(db)

    user = await repo.get_user_by_id(
        UUID(user_id)
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    if not user.is_active:

        raise HTTPException(
            status_code=403,
            detail="Account disabled",
        )

    return user


CurrentUserDep = Annotated[
    object,
    Depends(get_current_user),
]

# =========================================================
# Optional User
# =========================================================

async def get_optional_user(
    authorization: str | None = Header(
        default=None,
    ),
    db: AsyncSession = Depends(
        get_async_session
    ),
):

    if not authorization:
        return None

    try:

        token = extract_bearer_token(
            authorization
        )

        payload = validate_access_token(
            token
        )

        user_id = payload.get(
            "sub"
        )

        repo = UserRepository(db)

        return await repo.get_user_by_id(
            UUID(user_id)
        )

    except Exception:

        return None


OptionalUserDep = Annotated[
    object | None,
    Depends(get_optional_user),
]

# =========================================================
# Verified User
# =========================================================

async def require_verified_user(
    user: CurrentUserDep,
):

    if not user.is_verified:

        raise HTTPException(
            status_code=403,
            detail="Email verification required",
        )

    return user


VerifiedUserDep = Annotated[
    object,
    Depends(require_verified_user),
]

# =========================================================
# Admin
# =========================================================

async def require_admin(
    user: CurrentUserDep,
):

    role = getattr(
        user,
        "role",
        "member",
    )

    if role not in [
        "owner",
        "admin",
    ]:

        raise HTTPException(
            status_code=403,
            detail="Admin required",
        )

    return user


AdminUserDep = Annotated[
    object,
    Depends(require_admin),
]

# =========================================================
# Owner
# =========================================================

async def require_owner(
    user: CurrentUserDep,
):

    role = getattr(
        user,
        "role",
        "member",
    )

    if role != "owner":

        raise HTTPException(
            status_code=403,
            detail="Owner required",
        )

    return user


OwnerUserDep = Annotated[
    object,
    Depends(require_owner),
]

# =========================================================
# Pagination
# =========================================================

from app.core.pagination import (
    PaginationParams,
)

PaginationDep = Annotated[
    PaginationParams,
    Depends(),
]