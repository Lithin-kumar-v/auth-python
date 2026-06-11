# backend/app/oauth/service.py

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.oauth.repository import OAuthRepository
from app.oauth.schemas import OAuthProviderUser

from app.users.repository import UserRepository
from app.sessions.service import SessionService

from app.common.utils import (
    normalize_email,
    normalize_username,
    utc_now,
)

from uuid import UUID

from datetime import timedelta

from app.core.config import settings

from app.core.security import (
    create_token_pair,
    hash_password,
    validate_password_strength,
)

from app.core.exceptions import (
    UnauthorizedError,
    ValidationError,
    UserNotFoundError,
)


class OAuthService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

        self.oauth = OAuthRepository(
            db
        )

        self.users = UserRepository(
            db
        )

        self.sessions = SessionService(
            db
        )

    def _get_refresh_expiry(
        self,
    ):

        return utc_now() + timedelta(
            days=settings.REFRESH_TOKEN_DAYS
        )
    
    # =====================================================
    # HELPERS
    # =====================================================

    async def _create_login_response(
        self,
        *,
        user,
        login_method: str,
    ):

        tokens = create_token_pair(
            user_id=str(user.id),
            email=user.email,
            username=user.username,
            role="member",
        )

        await self.sessions.create_login_session(
            user=user,
            refresh_token=tokens[
                "refresh_token"
            ],
            expires_at=self._get_refresh_expiry(),
            login_method=login_method,
        )

        return {
            **tokens,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "auth_provider": user.auth_provider,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            },
        }

    async def _ensure_unique_username(
        self,
        username: str,
    ) -> str:

        username = normalize_username(
            username
        )

        if not await self.users.username_exists(
            username
        ):
            return username

        base_username = username

        counter = 1

        while await self.users.username_exists(
            username
        ):
            username = (
                f"{base_username}_{counter}"
            )

            counter += 1

        return username

    # =====================================================
    # GOOGLE LOGIN
    # =====================================================

    async def login_google(
        self,
        provider_user: OAuthProviderUser,
    ):

        user = (
            await self.oauth
            .get_user_by_google_id(
                provider_user.provider_id
            )
        )

        if user:

            if not user.is_active:
                raise UnauthorizedError(
                    "Account disabled"
                )

            await self.users.update_last_login(
                user_id=user.id,
                login_time=utc_now(),
            )

            return await self._create_login_response(
                user=user,
                login_method="google",
            )

        email = normalize_email(
            provider_user.email
        )

        user = await self.users.get_user_by_email(
            email
        )

        if user:

            if not user.is_active:
                raise UnauthorizedError(
                    "Account disabled"
                )

            await self.oauth.set_google_id(
                user_id=user.id,
                google_id=provider_user.provider_id,
            )

            await self.users.update_last_login(
                user_id=user.id,
                login_time=utc_now(),
            )

            return await self._create_login_response(
                user=user,
                login_method="google",
            )

        username = await self._ensure_unique_username(
            provider_user.username
        )

        user = await self.users.create_user(
            email=email,
            username=username,
            password_hash=None,
        )

        await self.users.create_profile(
            user_id=user.id,
            display_name=(
                provider_user.display_name
                or username
            ),
        )

        await self.users.mark_verified(
            user_id=user.id
        )

        await self.oauth.set_google_id(
            user_id=user.id,
            google_id=provider_user.provider_id,
        )

        return await self._create_login_response(
            user=user,
            login_method="google",
        )

    # =====================================================
    # GITHUB LOGIN
    # =====================================================

    async def login_github(
        self,
        provider_user: OAuthProviderUser,
    ):

        user = (
            await self.oauth
            .get_user_by_github_id(
                provider_user.provider_id
            )
        )

        if user:

            if not user.is_active:
                raise UnauthorizedError(
                    "Account disabled"
                )

            await self.users.update_last_login(
                user_id=user.id,
                login_time=utc_now(),
            )

            return await self._create_login_response(
                user=user,
                login_method="github",
            )

        email = normalize_email(
            provider_user.email
        )

        user = await self.users.get_user_by_email(
            email
        )

        if user:

            if not user.is_active:
                raise UnauthorizedError(
                    "Account disabled"
                )

            await self.oauth.set_github_id(
                user_id=user.id,
                github_id=provider_user.provider_id,
            )

            await self.users.update_last_login(
                user_id=user.id,
                login_time=utc_now(),
            )

            return await self._create_login_response(
                user=user,
                login_method="github",
            )

        username = await self._ensure_unique_username(
            provider_user.username
        ) 

        user = await self.users.create_user(
            email=email,
            username=username,
            password_hash=None,
        )

        await self.users.create_profile(
            user_id=user.id,
            display_name=(
                provider_user.display_name
                or username
            ),
        )

        await self.users.mark_verified(
            user_id=user.id
        )

        await self.oauth.set_github_id(
            user_id=user.id,
            github_id=provider_user.provider_id,
        )

        return await self._create_login_response(
            user=user,
            login_method="github",
        )

    # =====================================================
    # LINK GOOGLE
    # =====================================================

    async def link_google(
        self,
        *,
        user_id: UUID,
        google_id: str,
    ):
        
        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )

        exists = (
            await self.oauth
            .google_id_exists(
                google_id
            )
        )

        if exists:
            raise ValidationError(
                message=(
                    "Google account already linked"
                )
            )

        await self.oauth.set_google_id(
            user_id=user_id,
            google_id=google_id,
        )

        return {
            "success": True,
            "provider": "google",
            "message": (
                "Google linked successfully"
            ),
        }

    # =====================================================
    # LINK GITHUB
    # =====================================================

    async def link_github(
        self,
        *,
        user_id: UUID,
        github_id: str,
    ):
        
        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )

        exists = (
            await self.oauth
            .github_id_exists(
                github_id
            )
        )

        if exists:
            raise ValidationError(
                message=(
                    "GitHub account already linked"
                )
            )

        await self.oauth.set_github_id(
            user_id=user_id,
            github_id=github_id,
        )

        return {
            "success": True,
            "provider": "github",
            "message": (
                "GitHub linked successfully"
            ),
        }

    # =====================================================
    # UNLINK GOOGLE
    # =====================================================

    async def unlink_google(
        self,
        *,
        user_id: UUID,
    ):

        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )

        # ==========================================
        # Google Link Validation
        # ==========================================

        if not user.google_id:
            raise ValidationError(
                message=(
                    "Google account is not linked"
                )
            )

        if (
            not user.password_hash
            and not user.github_id
        ):
            raise ValidationError(
                message=(
                    "Cannot remove last login method"
                )
            )

        await self.oauth.unlink_google(
            user_id=user_id
        )

        if user.github_id:

            await self.oauth.set_auth_provider(
                user_id=user.id,
                provider="github",
            )

        else:

            await self.oauth.set_auth_provider(
                user_id=user.id,
                provider="password",
            )

        return {
            "success": True,
            "provider": "google",
            "message": (
                "Google account unlinked"
            ),
        }

    # =====================================================
    # UNLINK GITHUB
    # =====================================================

    async def unlink_github(
        self,
        *,
        user_id: UUID,
    ):

        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )

        # ==========================================
        # GitHub Link Validation
        # ==========================================

        if not user.github_id:
            raise ValidationError(
                message=(
                    "GitHub account is not linked"
                )
            )

        if (
            not user.password_hash
            and not user.google_id
        ):
            raise ValidationError(
                message=(
                    "Cannot remove last login method"
                )
            )

        await self.oauth.unlink_github(
            user_id=user_id
        )

        if user.google_id:

            await self.oauth.set_auth_provider(
                user_id=user.id,
                provider="google",
            )

        else:

            await self.oauth.set_auth_provider(
                user_id=user.id,
                provider="password",
            )

        return {
            "success": True,
            "provider": "github",
            "message": (
                "GitHub account unlinked"
            ),
        }

    # =====================================================
    # PASSWORD SETUP
    # =====================================================

    async def set_password(
        self,
        *,
        user_id: UUID,
        password: str,
    ):

        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )

        # ==========================================
        # Existing Password Validation
        # ==========================================

        if user.password_hash:
            raise ValidationError(
                message=(
                    "Password already configured"
                )
            )

        if not validate_password_strength(
            password
        ):
            raise ValidationError(
                message="Weak password"
            )

        password_hash = hash_password(
            password
        )

        await self.users.update_user(
            user_id=user_id,
            values={
                "password_hash": password_hash,
            },
        )

        return {
            "success": True,
            "message": (
                "Password configured"
            ),
        }
        
    # =====================================================
    # LINKED PROVIDERS
    # =====================================================

    async def get_linked_providers(
        self,
        *,
        user_id: UUID,
    ):

        user = await self.users.get_user_by_id(
            user_id
        )

        if not user:
            raise UserNotFoundError(
                str(user_id)
            )

        return {
            "password": bool(
                user.password_hash
            ),
            "google": bool(
                user.google_id
            ),
            "github": bool(
                user.github_id
            ),
            "auth_provider": (
                user.auth_provider
            ),
        }