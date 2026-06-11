from __future__ import annotations

from datetime import datetime
from datetime import timezone
from uuid import UUID

from sqlalchemy import exists
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


# =========================================================
# Helpers
# =========================================================

def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


# =========================================================
# OAuth Repository
# =========================================================

class OAuthRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # =====================================================
    # LOOKUPS
    # =====================================================

    async def get_user_by_google_id(
        self,
        google_id: str,
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(
                User.google_id == google_id
            )
        )

        return result.scalar_one_or_none()

    async def get_user_by_github_id(
        self,
        github_id: str,
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(
                User.github_id == github_id
            )
        )

        return result.scalar_one_or_none()

    async def get_user_by_provider(
        self,
        *,
        provider: str,
        provider_id: str,
    ) -> User | None:

        if provider == "google":
            return await self.get_user_by_google_id(
                provider_id
            )

        if provider == "github":
            return await self.get_user_by_github_id(
                provider_id
            )

        return None

    # =====================================================
    # EXISTS
    # =====================================================

    async def google_id_exists(
        self,
        google_id: str,
    ) -> bool:

        result = await self.db.execute(
            select(
                exists().where(
                    User.google_id == google_id
                )
            )
        )

        return bool(
            result.scalar()
        )

    async def github_id_exists(
        self,
        github_id: str,
    ) -> bool:

        result = await self.db.execute(
            select(
                exists().where(
                    User.github_id == github_id
                )
            )
        )

        return bool(
            result.scalar()
        )

    async def is_provider_linked(
        self,
        *,
        provider: str,
        provider_id: str,
    ) -> bool:

        if provider == "google":
            return await self.google_id_exists(
                provider_id
            )

        if provider == "github":
            return await self.github_id_exists(
                provider_id
            )

        return False

    # =====================================================
    # GOOGLE
    # =====================================================

    async def set_google_id(
        self,
        *,
        user_id: UUID,
        google_id: str,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                google_id=google_id,
                auth_provider="google",
                updated_at=utc_now(),
            )
        )

        await self.db.commit()

    async def unlink_google(
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
                google_id=None,
                updated_at=utc_now(),
            )
        )

        await self.db.commit()

    # =====================================================
    # GITHUB
    # =====================================================

    async def set_github_id(
        self,
        *,
        user_id: UUID,
        github_id: str,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                github_id=github_id,
                auth_provider="github",
                updated_at=utc_now(),
            )
        )

        await self.db.commit()

    async def unlink_github(
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
                github_id=None,
                updated_at=utc_now(),
            )
        )

        await self.db.commit()

    # =====================================================
    # PROVIDER
    # =====================================================

    async def set_auth_provider(
        self,
        *,
        user_id: UUID,
        provider: str,
    ) -> None:

        await self.db.execute(
            update(User)
            .where(
                User.id == user_id
            )
            .values(
                auth_provider=provider,
                updated_at=utc_now(),
            )
        )

        await self.db.commit()

    async def get_provider(
        self,
        user_id: UUID,
    ) -> str | None:

        result = await self.db.execute(
            select(
                User.auth_provider
            ).where(
                User.id == user_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # LOGIN TRACKING
    # =====================================================

    async def update_last_login(
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
                last_login_at=utc_now(),
                updated_at=utc_now(),
            )
        )

        await self.db.commit()


# =========================================================
# Export
# =========================================================

__all__ = [
    "OAuthRepository",
]