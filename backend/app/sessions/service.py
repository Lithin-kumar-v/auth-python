from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.sessions.repository import SessionRepository
from app.sessions.schemas import SessionStatsResponse

from app.users.repository import UserRepository

from app.common.utils import (
    sha256_hash,
)

from app.core.security import (
    create_token_pair,
    validate_refresh_token,
)

from app.core.exceptions import (
    UnauthorizedError,
    UserNotFoundError,
)


class SessionService:

    def __init__(
        self,
        db: AsyncSession,
    ):

        self.db = db

        self.sessions = SessionRepository(
            db
        )

        self.users = UserRepository(
            db
        )

    # =====================================================
    # CREATE LOGIN SESSION
    # =====================================================

    async def create_login_session(
        self,
        *,
        user,
        refresh_token: str,
        expires_at,
        login_method: str = "password",
        session_name: str | None = None,
        device_name: str | None = None,
        device_type: str | None = None,
        browser: str | None = None,
        browser_version: str | None = None,
        os: str | None = None,
        os_version: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
        country: str | None = None,
        region: str | None = None,
        city: str | None = None,
        timezone: str | None = None,
    ):

        session = await self.sessions.create_session(
            user_id=user.id,
            refresh_token_hash=sha256_hash(
                refresh_token
            ),
            token_family=str(
                uuid4()
            ),
            login_method=login_method,
            session_name=session_name,
            device_name=device_name,
            device_type=device_type,
            browser=browser,
            browser_version=browser_version,
            os=os,
            os_version=os_version,
            user_agent=user_agent,
            ip_address=ip_address,
            country=country,
            region=region,
            city=city,
            timezone=timezone,
            expires_at=expires_at,
        )

        await self.sessions.mark_current(
            user_id=user.id,
            session_id=session.id,
        )

        return session

    # =====================================================
    # LIST USER SESSIONS
    # =====================================================

    async def list_sessions(
        self,
        user_id: UUID,
    ):

        return await self.sessions.get_user_sessions(
            user_id
        )

    # =====================================================
    # CURRENT SESSION
    # =====================================================

    async def get_current_session(
        self,
        user_id: UUID,
    ):

        current = await self.sessions.get_current_session(
            user_id
        )

        if current:
            return current

        sessions = await self.sessions.get_active_user_sessions(
            user_id
        )

        if not sessions:
            return None

        latest_session = sessions[0]

        await self.sessions.mark_current(
            user_id=user_id,
            session_id=latest_session.id,
        )

        return await self.sessions.get_by_id(
            latest_session.id
        )

    # =====================================================
    # GET SESSION
    # =====================================================

    async def get_session(
        self,
        session_id: UUID,
    ):

        session = await self.sessions.get_by_id(
            session_id
        )

        if not session:
            raise UnauthorizedError(
                "Session not found"
            )

        return session

    # =====================================================
    # LOGOUT DEVICE
    # =====================================================

    async def logout_device(
        self,
        *,
        user_id: UUID,
        session_id: UUID,
    ):

        session = await self.sessions.get_by_id(
            session_id
        )

        if not session:
            raise UnauthorizedError(
                "Session not found"
            )

        if session.user_id != user_id:
            raise UnauthorizedError(
                "Not allowed"
            )

        await self.sessions.revoke_session(
            session_id=session_id,
            reason="device_logout",
        )

        return {
            "success": True,
            "message": "Device logged out",
        }

    # =====================================================
    # LOGOUT ALL DEVICES
    # =====================================================

    async def logout_all_devices(
        self,
        user_id: UUID,
    ):

        count = (
            await self.sessions
            .revoke_all_user_sessions(
                user_id=user_id,
                reason="logout_all",
            )
        )

        return {
            "success": True,
            "revoked_sessions": count,
        }

    # =====================================================
    # REFRESH ROTATION
    # =====================================================

    async def rotate_refresh_token(
        self,
        refresh_token: str,
    ):

        payload = validate_refresh_token(
            refresh_token
        )

        user_id = payload.get(
            "sub"
        )

        if not user_id:
            raise UnauthorizedError(
                "Invalid refresh token"
            )

        user = await self.users.get_user_by_id(
            UUID(user_id)
        )

        if not user:
            raise UserNotFoundError(
                user_id
            )

        session = (
            await self.sessions
            .get_active_session_by_hash(
                sha256_hash(
                    refresh_token
                )
            )
        )

        if not session:
            raise UnauthorizedError(
                "Session not found"
            )

        tokens = create_token_pair(
            user_id=str(user.id),
            email=user.email,
            username=user.username,
            role="member",
        )

        new_hash = sha256_hash(
            tokens["refresh_token"]
        )

        await self.sessions.rotate_session(
            session_id=session.id,
            new_token_hash=new_hash,
        )

        return {
            **tokens,
            "user": user,
        }

    # =====================================================
    # MARK SUSPICIOUS
    # =====================================================

    async def mark_suspicious(
        self,
        session_id: UUID,
    ):

        await self.sessions.mark_suspicious(
            session_id
        )

        return {
            "success": True,
            "message": (
                "Session marked suspicious"
            ),
        }

    # =====================================================
    # SESSION STATS
    # =====================================================

    async def get_stats(
        self,
        user_id: UUID,
    ) -> SessionStatsResponse:

        sessions = (
            await self.sessions
            .get_user_sessions(user_id)
        )

        total = len(sessions)

        active = len(
            [
                s
                for s in sessions
                if not s.revoked
            ]
        )

        revoked = len(
            [
                s
                for s in sessions
                if s.revoked
            ]
        )

        suspicious = len(
            [
                s
                for s in sessions
                if s.suspicious
            ]
        )

        return SessionStatsResponse(
            total_sessions=total,
            active_sessions=active,
            revoked_sessions=revoked,
            suspicious_sessions=suspicious,
        )
    
    # =====================================================
    # CLEANUP
    # =====================================================

    async def cleanup_expired_sessions(
        self,
    ):

        deleted = (
            await self.sessions
            .delete_expired_sessions()
        )

        return {
            "deleted_sessions":
            deleted
        }