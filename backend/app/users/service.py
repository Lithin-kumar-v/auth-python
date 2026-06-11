from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.users.repository import UserRepository

from app.core.exceptions import (
    UserNotFoundError,
)

from app.users.schemas import (
    UserResponse,
    UserProfileResponse,
    UserDetailResponse,
    UserSummaryResponse,
)

from app.common.utils import (
    remove_none_values,
)


class UserService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.repo = UserRepository(db)

    # =====================================================
    # GET USER
    # =====================================================

    async def get_user(
        self,
        user_id: UUID,
    ) -> UserResponse:

        user = await self.repo.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )
        

        return UserResponse.model_validate(
            user
        )

    # =====================================================
    # GET PROFILE
    # =====================================================

    async def get_profile(
        self,
        user_id: UUID,
    ) -> UserProfileResponse:

        profile = await self.repo.get_profile(
            user_id
        )

        if not profile:
            raise UserNotFoundError(
                str(user_id)
            )

        return UserProfileResponse.model_validate(
            profile
        )

    # =====================================================
    # GET USER DETAIL
    # =====================================================

    async def get_user_detail(
        self,
        user_id: UUID,
    ) -> UserDetailResponse:

        result = await self.repo.get_user_with_profile(
            user_id
        )

        if not result:
            raise UserNotFoundError(
                str(user_id)
            )

        user = result["user"]
        profile = result["profile"]

        return UserDetailResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            auth_provider=user.auth_provider,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at,
            profile=(
                UserProfileResponse.model_validate(
                    profile
                )
                if profile
                else None
            ),
        )

    # =====================================================
    # LIST USERS
    # =====================================================

    async def list_users(
        self,
        *,
        page: int = 1,
        limit: int = 20,
    ):

        offset = (
            page - 1
        ) * limit

        users = await self.repo.list_users(
            offset=offset,
            limit=limit,
        )

        total = await self.repo.count_users()

        return {
            "items": [
                UserSummaryResponse.model_validate(
                    user
                )
                for user in users
            ],
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (
                (total + limit - 1)
                // limit
            ),
        }

    # =====================================================
    # UPDATE USER
    # =====================================================

    async def update_user(
        self,
        *,
        user_id: UUID,
        values: dict,
    ) -> UserResponse:

        values = remove_none_values(
            values
        )

        exists = await self.repo.user_exists(
            user_id
        )

        if not exists:
            raise UserNotFoundError(
                str(user_id)
            )

        user = await self.repo.update_user(
            user_id=user_id,
            values=values,
        )

        return UserResponse.model_validate(
            user
        )

    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    async def update_profile(
        self,
        *,
        user_id: UUID,
        values: dict,
    ) -> UserProfileResponse:

        values = remove_none_values(
            values
        )

        profile = await self.repo.update_profile(
            user_id=user_id,
            values=values,
        )

        if not profile:
            raise UserNotFoundError(
                str(user_id)
            )

        return UserProfileResponse.model_validate(
            profile
        )

    # =====================================================
    # ACTIVATE USER
    # =====================================================

    async def activate_user(
        self,
        user_id: UUID,
    ):

        exists = await self.repo.user_exists(
            user_id
        )

        if not exists:
            raise UserNotFoundError(
                str(user_id)
            )

        await self.repo.activate_user(
            user_id=user_id
        )

        return {
            "message": "User activated"
        }

    # =====================================================
    # DEACTIVATE USER
    # =====================================================

    async def deactivate_user(
        self,
        user_id: UUID,
    ):

        exists = await self.repo.user_exists(
            user_id
        )

        if not exists:
            raise UserNotFoundError(
                str(user_id)
            )

        await self.repo.deactivate_user(
            user_id=user_id
        )

        return {
            "message": "User deactivated"
        }

    # =====================================================
    # VERIFY USER
    # =====================================================

    async def verify_user(
        self,
        user_id: UUID,
    ):

        exists = await self.repo.user_exists(
            user_id
        )

        if not exists:
            raise UserNotFoundError(
                str(user_id)
            )

        await self.repo.mark_verified(
            user_id=user_id
        )

        return {
            "message": "User verified"
        }

    # =====================================================
    # DELETE USER
    # =====================================================

    async def delete_user(
        self,
        user_id: UUID,
    ):

        exists = await self.repo.user_exists(
            user_id
        )

        if not exists:
            raise UserNotFoundError(
                str(user_id)
            )

        await self.repo.delete_user(
            user_id=user_id
        )

        return {
            "message": "User deleted"
        }

    # =====================================================
    # USER STATS
    # =====================================================

    async def get_user_stats(
        self,
    ):

        total_users = await self.repo.count_users()

        verified_users = (
            await self.repo.count_verified_users()
        )

        active_users = (
            await self.repo.count_active_users()
        )

        return {
            "total_users": total_users,
            "verified_users": verified_users,
            "active_users": active_users,
        }

    # =====================================================
    # SEARCH USER BY EMAIL
    # =====================================================

    async def find_user_by_email(
        self,
        email: str,
    ) -> UserResponse:

        user = await self.repo.get_user_by_email(
            email
        )

        if not user:
            raise UserNotFoundError(
                email
            )

        return UserResponse.model_validate(
            user
        )

    # =====================================================
    # SEARCH USER BY USERNAME
    # =====================================================

    async def find_user_by_username(
        self,
        username: str,
    ) -> UserResponse:

        user = await self.repo.get_user_by_username(
            username
        )

        if not user:
            raise UserNotFoundError(
                username
            )

        return UserResponse.model_validate(
            user
        )