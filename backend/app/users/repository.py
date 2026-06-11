from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import exists
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.models import UserProfile

from app.common.utils import (
    remove_none_values,
)

from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    async def create_user(
        self,
        *,
        email: str,
        username: str,
        password_hash: str | None,
    ) -> User:

        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
        )

        self.db.add(user)

        try:

            await self.db.commit()

        except IntegrityError:

            await self.db.rollback()

            raise UserAlreadyExistsError(
                email=email
            )

        await self.db.refresh(user)

        return user

    async def create_profile(
        self,
        *,
        user_id: UUID,
        display_name: str | None = None,
    ) -> UserProfile:

        profile = UserProfile(
            user_id=user_id,
            display_name=display_name,
        )

        self.db.add(profile)

        await self.db.commit()

        await self.db.refresh(profile)

        return profile

    async def create_user_with_profile(
        self,
        *,
        email: str,
        username: str,
        password_hash: str | None,
    ) -> User:

        try:

            user = User(
                email=email,
                username=username,
                password_hash=password_hash,
            )

            self.db.add(user)

            await self.db.flush()

            profile = UserProfile(
                user_id=user.id,
                display_name=username,
            )

            self.db.add(profile)

            await self.db.commit()

            await self.db.refresh(user)

            return user

        except IntegrityError:

            await self.db.rollback()

            raise UserAlreadyExistsError(
                email=email
            )

    # =====================================================
    # READ
    # =====================================================

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        result = await self.db.execute(
            select(User)
            .where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_user_for_update(
        self,
        user_id: UUID,
    ) -> User | None:

        result = await self.db.execute(
            select(User)
            .where(
                User.id == user_id
            )
            .with_for_update()
        )

        return result.scalar_one_or_none()

    async def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        result = await self.db.execute(
            select(User)
            .where(
                User.email == email
            )
        )

        return result.scalar_one_or_none()

    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:

        result = await self.db.execute(
            select(User)
            .where(
                User.username == username
            )
        )

        return result.scalar_one_or_none()

    async def get_profile(
        self,
        user_id: UUID,
    ) -> UserProfile | None:

        result = await self.db.execute(
            select(UserProfile)
            .where(
                UserProfile.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_user_with_profile(
        self,
        user_id: UUID,
    ) -> dict | None:

        result = await self.db.execute(
            select(
                User,
                UserProfile,
            )
            .outerjoin(
                UserProfile,
                User.id == UserProfile.user_id,
            )
            .where(
                User.id == user_id
            )
        )

        row = result.first()

        if not row:
            return None

        user, profile = row

        return {
            "user": user,
            "profile": profile,
        }

    async def list_users(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:

        result = await self.db.execute(
            select(User)
            .order_by(
                User.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        return (
            result.scalars()
            .all()
        )

    async def count_users(
        self,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(User.id)
            )
        )

        return int(
            result.scalar() or 0
        )

    # =====================================================
    # EXISTS
    # =====================================================

    async def user_exists(
        self,
        user_id: UUID,
    ) -> bool:

        result = await self.db.execute(
            select(
                exists().where(
                    User.id == user_id
                )
            )
        )

        return bool(
            result.scalar()
        )

    async def email_exists(
        self,
        email: str,
    ) -> bool:

        result = await self.db.execute(
            select(
                exists().where(
                    User.email == email
                )
            )
        )

        return bool(
            result.scalar()
        )

    async def username_exists(
        self,
        username: str,
    ) -> bool:

        result = await self.db.execute(
            select(
                exists().where(
                    User.username == username
                )
            )
        )

        return bool(
            result.scalar()
        )

    # =====================================================
    # UPDATE
    # =====================================================

    async def update_user(
        self,
        *,
        user_id: UUID,
        values: dict,
    ) -> User:

        values = remove_none_values(
            values
        )

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(**values)
        )

        await self.db.commit()

        user = await self.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                user_id
            )

        return user

    async def update_profile(
        self,
        *,
        user_id: UUID,
        values: dict,
    ) -> UserProfile:

        values = remove_none_values(
            values
        )

        await self.db.execute(
            update(UserProfile)
            .where(
                UserProfile.user_id == user_id
            )
            .values(**values)
        )

        await self.db.commit()

        profile = await self.get_profile(
            user_id
        )

        if not profile:
            raise UserNotFoundError(
                user_id
            )

        return profile

    # =====================================================
    # STATUS
    # =====================================================

    async def update_last_login(
        self,
        *,
        user_id: UUID,
        login_time: datetime,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                last_login_at=login_time
            )
        )

        await self.db.commit()

    async def mark_verified(
        self,
        *,
        user_id: UUID,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                is_verified=True
            )
        )

        await self.db.commit()

    async def activate_user(
        self,
        *,
        user_id: UUID,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                is_active=True
            )
        )

        await self.db.commit()

    async def deactivate_user(
        self,
        *,
        user_id: UUID,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                is_active=False
            )
        )

        await self.db.commit()

    # =====================================================
    # DELETE
    # =====================================================

    async def delete_user(
        self,
        *,
        user_id: UUID,
    ) -> None:

        await self.db.execute(
            delete(User)
            .where(
                User.id == user_id
            )
        )

        await self.db.commit()