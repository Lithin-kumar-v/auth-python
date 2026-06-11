from __future__ import annotations

from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import (
    LoginRequest,
    RegisterRequest,
)

from app.sessions.service import SessionService

from app.users.repository import UserRepository

from app.common.utils import (
    normalize_email,
    normalize_username,
    utc_now,
)

from app.core.security import (
    create_token_pair,
    hash_password,
    validate_password_strength,
    verify_password,
)

from app.core.exceptions import (
    InvalidCredentialsError,
    UnauthorizedError,
    UserAlreadyExistsError,
    UserNotFoundError,
    ValidationError,
)


class AuthService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.users = UserRepository(db)

    # =====================================================
    # HELPERS
    # =====================================================

    def _get_refresh_expiry(
        self,
    ):
        return utc_now() + timedelta(
            days=30
        )

    # =====================================================
    # REGISTER
    # =====================================================

    async def register(
        self,
        payload: RegisterRequest,
    ):

        email = normalize_email(
            payload.email
        )

        username = normalize_username(
            payload.username
        )

        if await self.users.email_exists(
            email
        ):
            raise UserAlreadyExistsError(
                email
            )

        if await self.users.username_exists(
            username
        ):
            raise ValidationError(
                message="Username already exists"
            )

        if not validate_password_strength(
            payload.password
        ):
            raise ValidationError(
                message=(
                    "Password must contain uppercase, "
                    "lowercase and number"
                )
            )

        password_hash = hash_password(
            payload.password
        )

        user = await self.users.create_user(
            email=email,
            username=username,
            password_hash=password_hash,
        )

        await self.users.create_profile(
            user_id=user.id,
            display_name=username,
        )

        tokens = create_token_pair(
            user_id=str(user.id),
            email=user.email,
            username=user.username,
            role="member",
        )

        session_service = SessionService(
            self.db
        )

        await session_service.create_login_session(
            user=user,
            refresh_token=tokens[
                "refresh_token"
            ],
            expires_at=self._get_refresh_expiry(),
            login_method="password",
        )

        return {
            **tokens,
            "user": user,
        }

    # =====================================================
    # LOGIN
    # =====================================================

    async def login(
        self,
        payload: LoginRequest,
    ):

        email = normalize_email(
            payload.email
        )

        user = await self.users.get_user_by_email(
            email
        )

        if not user:
            raise InvalidCredentialsError()

        if not user.is_active:
            raise UnauthorizedError(
                "Account disabled"
            )

        if not user.password_hash:
            raise UnauthorizedError(
                "PASSWORD_NOT_SET"
            )

        if not verify_password(
            payload.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError()

        await self.users.update_last_login(
            user_id=user.id,
            login_time=utc_now(),
        )

        tokens = create_token_pair(
            user_id=str(user.id),
            email=user.email,
            username=user.username,
            role="member",
        )

        session_service = SessionService(
            self.db
        )

        await session_service.create_login_session(
            user=user,
            refresh_token=tokens[
                "refresh_token"
            ],
            expires_at=self._get_refresh_expiry(),
            login_method="password",
        )

        return {
            **tokens,
            "user": user,
        }

    # =====================================================
    # REFRESH TOKEN
    # =====================================================

    async def refresh_token(
        self,
        refresh_token: str,
    ):

        session_service = SessionService(
            self.db
        )

        return await session_service.rotate_refresh_token(
            refresh_token
        )

    # =====================================================
    # LOGOUT
    # =====================================================

    async def logout(
        self,
        *,
        user_id: UUID,
        session_id: UUID,
    ):

        session_service = SessionService(
            self.db
        )

        await session_service.logout_device(
            user_id=user_id,
            session_id=session_id,
        )

        return {
            "message":
            "Logged out successfully"
        }

    # =====================================================
    # VERIFY EMAIL
    # =====================================================

    async def verify_email(
        self,
        user_id: UUID,
    ):

        await self.users.mark_verified(
            user_id=user_id
        )

        return {
            "message": "Email verified"
        }

    # =====================================================
    # ACTIVATE USER
    # =====================================================

    async def activate_user(
        self,
        user_id: UUID,
    ):

        await self.users.activate_user(
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

        await self.users.deactivate_user(
            user_id=user_id
        )

        return {
            "message": "User deactivated"
        }

    # =====================================================
    # CHANGE PASSWORD
    # =====================================================

    async def change_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ):

        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                user_id
            )

        if not user.password_hash:
            raise UnauthorizedError(
                "PASSWORD_NOT_SET"
            )

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            raise InvalidCredentialsError()

        if not validate_password_strength(
            new_password
        ):
            raise ValidationError(
                message="Weak password"
            )

        password_hash = hash_password(
            new_password
        )

        await self.users.update_user(
            user_id=user.id,
            values={
                "password_hash": password_hash,
            },
        )

        return {
            "message":
            "Password updated successfully"
        }

    # =====================================================
    # GET USER
    # =====================================================

    async def get_user(
        self,
        user_id: UUID,
    ):

        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                user_id
            )

        return user

    # =====================================================
    # GET USER WITH PROFILE
    # =====================================================

    async def get_user_with_profile(
        self,
        user_id: UUID,
    ):

        user = await self.users.get_user_with_profile(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                user_id
            )

        return user