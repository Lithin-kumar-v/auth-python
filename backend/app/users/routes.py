from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Query
from fastapi import status

from app.common.dependencies import (
    DatabaseDep,
    CurrentUserDep,
)

from app.core.responses import (
    success_response,
)

from app.users.schemas import (
    UserUpdate,
    UserProfileUpdate,
)

from app.users.service import (
    UserService,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# =====================================================
# CURRENT USER
# =====================================================

@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
async def get_me(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = UserService(db)

    user = await service.get_user(
        current_user.id
    )

    return success_response(
        data=user,
    )


# =====================================================
# CURRENT PROFILE
# =====================================================

@router.get(
    "/me/profile",
    status_code=status.HTTP_200_OK,
    summary="Get current profile",
)
async def get_my_profile(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = UserService(db)

    profile = await service.get_profile(
        current_user.id
    )

    return success_response(
        data=profile,
    )


# =====================================================
# UPDATE PROFILE
# =====================================================

@router.patch(
    "/me/profile",
    status_code=status.HTTP_200_OK,
    summary="Update current profile",
)
async def update_my_profile(
    payload: UserProfileUpdate,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = UserService(db)

    profile = await service.update_profile(
        user_id=current_user.id,
        values=payload.model_dump(
            exclude_none=True,
        ),
    )

    return success_response(
        data=profile,
        message="Profile updated successfully",
    )


# =====================================================
# UPDATE USER
# =====================================================

@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Update current user",
)
async def update_me(
    payload: UserUpdate,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = UserService(db)

    user = await service.update_user(
        user_id=current_user.id,
        values=payload.model_dump(
            exclude_none=True,
        ),
    )

    return success_response(
        data=user,
        message="User updated successfully",
    )


# =====================================================
# SEARCH EMAIL
# MUST STAY ABOVE /{user_id}
# =====================================================

@router.get(
    "/search/email",
    status_code=status.HTTP_200_OK,
    summary="Find user by email",
)
async def get_user_by_email(
    email: str,
    db: DatabaseDep,
):

    service = UserService(db)

    user = await service.find_user_by_email(
        email
    )

    return success_response(
        data=user,
    )


# =====================================================
# SEARCH USERNAME
# MUST STAY ABOVE /{user_id}
# =====================================================

@router.get(
    "/search/username",
    status_code=status.HTTP_200_OK,
    summary="Find user by username",
)
async def get_user_by_username(
    username: str,
    db: DatabaseDep,
):

    service = UserService(db)

    user = await service.find_user_by_username(
        username
    )

    return success_response(
        data=user,
    )


# =====================================================
# ADMIN USER STATS
# MUST STAY ABOVE /{user_id}
# =====================================================

@router.get(
    "/admin/stats",
    status_code=status.HTTP_200_OK,
    summary="User statistics",
)
async def user_stats(
    db: DatabaseDep,
):

    service = UserService(db)

    stats = await service.get_user_stats()

    return success_response(
        data=stats,
    )


# =====================================================
# LIST USERS
# =====================================================

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="List users",
)
async def list_users(
    db: DatabaseDep,
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Items per page",
    ),
):

    service = UserService(db)

    users = await service.list_users(
        page=page,
        limit=limit,
    )

    return success_response(
        data=users,
    )


# =====================================================
# USER DETAIL
# KEEP BELOW STATIC ROUTES
# =====================================================

@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user detail",
)
async def get_user(
    user_id: UUID,
    db: DatabaseDep,
):

    service = UserService(db)

    user = await service.get_user_detail(
        user_id
    )

    return success_response(
        data=user,
    )


# =====================================================
# VERIFY USER
# =====================================================

@router.patch(
    "/{user_id}/verify",
    status_code=status.HTTP_200_OK,
    summary="Verify user",
)
async def verify_user(
    user_id: UUID,
    db: DatabaseDep,
):

    service = UserService(db)

    result = await service.verify_user(
        user_id
    )

    return success_response(
        data=result,
        message="User verified",
    )


# =====================================================
# ACTIVATE USER
# =====================================================

@router.patch(
    "/{user_id}/activate",
    status_code=status.HTTP_200_OK,
    summary="Activate user",
)
async def activate_user(
    user_id: UUID,
    db: DatabaseDep,
):

    service = UserService(db)

    result = await service.activate_user(
        user_id
    )

    return success_response(
        data=result,
        message="User activated",
    )


# =====================================================
# DEACTIVATE USER
# =====================================================

@router.patch(
    "/{user_id}/deactivate",
    status_code=status.HTTP_200_OK,
    summary="Deactivate user",
)
async def deactivate_user(
    user_id: UUID,
    db: DatabaseDep,
):

    service = UserService(db)

    result = await service.deactivate_user(
        user_id
    )

    return success_response(
        data=result,
        message="User deactivated",
    )


# =====================================================
# DELETE USER
# =====================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user",
)
async def delete_user(
    user_id: UUID,
    db: DatabaseDep,
):

    service = UserService(db)

    result = await service.delete_user(
        user_id
    )

    return success_response(
        data=result,
        message="User deleted",
    )