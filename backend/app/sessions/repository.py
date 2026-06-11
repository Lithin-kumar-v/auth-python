from __future__ import annotations

from app.common.utils import utc_now
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession

from app.sessions.models import UserSession


class SessionRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        **kwargs,
    ) -> UserSession:

        session = UserSession(
            **kwargs
        )

        self.db.add(
            session
        )

        await self.db.flush()

        await self.db.refresh(
            session
        )

        await self.db.commit()

        return session

    # =====================================================
    # Get By Id
    # =====================================================

    async def get_by_id(
        self,
        session_id: UUID,
    ) -> UserSession | None:

        result = await self.db.execute(
            select(UserSession).where(
                UserSession.id == session_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get By Refresh Hash
    # =====================================================

    async def get_by_refresh_hash(
        self,
        refresh_token_hash: str,
    ) -> UserSession | None:

        result = await self.db.execute(
            select(UserSession).where(
                UserSession.refresh_token_hash
                == refresh_token_hash
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Get User Sessions
    # =====================================================

    async def get_user_sessions(
        self,
        user_id: UUID,
    ) -> list[UserSession]:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.user_id == user_id
            )
            .order_by(
                UserSession.last_activity.desc()
            )
        )

        return list(
            result.scalars().all()
        )

    async def get_active_user_sessions(
        self,
        user_id: UUID,
    ) -> list[UserSession]:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.revoked.is_(False),
            )
            .order_by(
                UserSession.last_activity.desc()
            )
        )

        return list(
            result.scalars().all()
        )

    # =====================================================
    # CURRENT SESSION
    # =====================================================

    async def get_current_session(
        self,
        user_id: UUID,
    ) -> UserSession | None:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.is_current.is_(True),
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # Token Family
    # =====================================================

    async def get_by_token_family(
        self,
        token_family: str,
    ) -> list[UserSession]:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.token_family
                == token_family
            )
        )

        return list(
            result.scalars().all()
        )

    # =====================================================
    # Activity
    # =====================================================

    async def update_last_activity(
        self,
        session_id: UUID,
    ) -> None:

        await self.db.execute(
            update(UserSession)
            .where(
                UserSession.id == session_id
            )
            .values(
                last_activity=utc_now()
            )
        )

        await self.db.commit()

    async def mark_current(
        self,
        user_id: UUID,
        session_id: UUID,
    ) -> None:

        await self.db.execute(
            update(UserSession)
            .where(
                UserSession.user_id == user_id
            )
            .values(
                is_current=False
            )
        )

        await self.db.execute(
            update(UserSession)
            .where(
                UserSession.id == session_id
            )
            .values(
                is_current=True
            )
        )

        await self.db.commit()

    # =====================================================
    # Rotation
    # =====================================================

    async def rotate_session(
        self,
        session_id: UUID,
        new_token_hash: str,
    ) -> None:

        await self.db.execute(
            update(UserSession)
            .where(
                UserSession.id == session_id
            )
            .values(
                revoked=True,
                revoked_reason="rotated",
                revoked_at=utc_now(),
                replaced_by_token=new_token_hash,
            )
        )

        await self.db.commit()

    # =====================================================
    # Revoke
    # =====================================================

    async def revoke_session(
        self,
        session_id: UUID,
        reason: str = "logout",
    ) -> None:

        await self.db.execute(
            update(UserSession)
            .where(
                UserSession.id == session_id
            )
            .values(
                revoked=True,
                revoked_reason=reason,
                revoked_at=utc_now(),
            )
        )

        await self.db.commit()

    async def revoke_all_user_sessions(
        self,
        user_id: UUID,
        reason: str = "logout_all",
    ) -> int:

        result = await self.db.execute(
            update(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.revoked.is_(False),
            )
            .values(
                revoked=True,
                revoked_reason=reason,
                revoked_at=utc_now(),
            )
        )

        await self.db.commit()

        return result.rowcount or 0

    async def revoke_token_family(
        self,
        token_family: str,
        reason: str = "family_revoked",
    ) -> int:

        result = await self.db.execute(
            update(UserSession)
            .where(
                UserSession.token_family
                == token_family
            )
            .values(
                revoked=True,
                revoked_reason=reason,
                revoked_at=utc_now(),
            )
        )

        await self.db.commit()

        return result.rowcount or 0

    # =====================================================
    # Security
    # =====================================================

    async def mark_suspicious(
        self,
        session_id: UUID,
    ) -> None:

        await self.db.execute(
            update(UserSession)
            .where(
                UserSession.id == session_id
            )
            .values(
                suspicious=True
            )
        )

        await self.db.commit()

    async def get_suspicious_sessions(
        self,
    ) -> list[UserSession]:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.suspicious.is_(True)
            )
        )

        return list(
            result.scalars().all()
        )

    # =====================================================
    # Expiration
    # =====================================================

    async def get_expired_sessions(
        self,
    ) -> list[UserSession]:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.expires_at
                < utc_now()
            )
        )

        return list(
            result.scalars().all()
        )

    async def delete_expired_sessions(
        self,
    ) -> int:

        result = await self.db.execute(
            delete(UserSession)
            .where(
                UserSession.expires_at
                < utc_now()
            )
        )

        await self.db.commit()

        return result.rowcount or 0

    # =====================================================
    # Analytics
    # =====================================================

    async def count_active_sessions(
        self,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(
                    UserSession.id
                )
            ).where(
                UserSession.revoked.is_(False)
            )
        )

        return int(
            result.scalar() or 0
        )

    async def count_revoked_sessions(
        self,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(
                    UserSession.id
                )
            ).where(
                UserSession.revoked.is_(True)
            )
        )

        return int(
            result.scalar() or 0
        )

    async def count_suspicious_sessions(
        self,
    ) -> int:

        result = await self.db.execute(
            select(
                func.count(
                    UserSession.id
                )
            ).where(
                UserSession.suspicious.is_(True)
            )
        )

        return int(
            result.scalar() or 0
        )
    
    async def create_session(
        self,
        **kwargs,
    ) -> UserSession:

        return await self.create(
            **kwargs
        )


    async def get_active_session_by_hash(
        self,
        refresh_token_hash: str,
    ) -> UserSession | None:

        result = await self.db.execute(
            select(UserSession)
            .where(
                UserSession.refresh_token_hash
                == refresh_token_hash,
                UserSession.revoked.is_(False),
            )
        )

        return result.scalar_one_or_none()