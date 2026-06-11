from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session

from app.common.dependencies import (
    CurrentUserDep,
)

from app.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    CurrentUser,
)

from app.auth.service import AuthService

from app.core.responses import (
    success_response,
)

# =========================================================
# Router
# =========================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# =========================================================
# Dependency
# =========================================================

def get_auth_service(
    db: AsyncSession = Depends(
        get_async_session
    ),
) -> AuthService:

    return AuthService(db)


# =========================================================
# Register
# =========================================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    result = await service.register(
        payload
    )

    return success_response(
        data=result,
        message="User registered successfully",
    )


# =========================================================
# Login
# =========================================================

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    result = await service.login(
        payload
    )

    return success_response(
        data=result,
        message="Login successful",
    )


# =========================================================
# Refresh Token
# =========================================================

@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh(
    payload: RefreshTokenRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):

    result = await service.refresh_token(
        payload.refresh_token
    )

    return success_response(
        data=result,
        message="Token refreshed",
    )


# =========================================================
# Logout Current Device
# =========================================================

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    current_user: CurrentUserDep,
    service: AuthService = Depends(
        get_auth_service,
    ),
    session_id: UUID = Query(
        ...,
        description="Session ID to logout",
    ),
):

    result = await service.logout(
        user_id=current_user.id,
        session_id=session_id,
    )

    return success_response(
        data=result,
        message="Logout successful",
    )

# =========================================================
# Get Current User
# =========================================================

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
async def get_me(
    current_user: CurrentUserDep,
):

    return success_response(
    data=CurrentUser.model_validate(
        current_user
    ),
    message="Current user",
)


# =========================================================
# Health Check
# =========================================================

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def auth_health():

    return success_response(
        data={
            "service": "auth",
            "status": "healthy",
        },
        message="Auth service healthy",
    )