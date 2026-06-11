from __future__ import annotations

from fastapi import APIRouter
from fastapi import Request
from fastapi import status

from app.common.dependencies import (
    CurrentUserDep,
    DatabaseDep,
)

from app.core.responses import (
    success_response,
)

from app.oauth.providers import (
    get_google_provider,
    get_github_provider,
)

from app.oauth.schemas import (
    GoogleUserInfo,
    GitHubUserInfo,
    OAuthProviderUser,
    PasswordSetupRequest,
)

from authlib.integrations.base_client.errors import (
    OAuthError,
)

from app.core.exceptions import (
    ValidationError,
)

from app.oauth.service import (
    OAuthService,
)

router = APIRouter(
    prefix="/oauth",
    tags=["OAuth"],
)

# =====================================================
# GOOGLE LOGIN URL
# =====================================================

@router.get(
    "/google/login",
    status_code=status.HTTP_200_OK,
)
async def google_login(
    request: Request,
):

    google = get_google_provider()

    return await google.authorize_redirect(
        request,
        request.url_for(
            "google_callback"
        ),
    )

# =====================================================
# GOOGLE CALLBACK
# =====================================================

@router.get(
    "/google/callback",
    name="google_callback",
)
async def google_callback(
    request: Request,
    db: DatabaseDep,
):

    google = get_google_provider()

    # ==========================================
    # USER CANCELLED AUTHORIZATION
    # ==========================================

    if request.query_params.get(
        "error"
    ):

        return success_response(
            data={
                "success": False,
                "provider": "google",
                "error":
                    request.query_params.get(
                        "error"
                    ),
            },
            message=request.query_params.get(
                "error_description",
                "Google authorization cancelled",
            ),
        )

    # ==========================================
    # EXCHANGE CODE FOR TOKEN
    # ==========================================

    try:

        token = await google.authorize_access_token(
            request
        )

    except OAuthError as exc:

        return success_response(
            data={
                "success": False,
                "provider": "google",
            },
            message=str(exc),
        )

    # ==========================================
    # USER INFO
    # ==========================================

    user_data = token.get(
        "userinfo"
    )

    if not user_data:

        user_data = await google.parse_id_token(
            request,
            token,
        )

    info = GoogleUserInfo.model_validate(
        user_data
    )

    provider_user = OAuthProviderUser(
        provider_id=info.sub,
        email=info.email,
        username=(
            info.email.split("@")[0]
        ),
        display_name=info.name,
        avatar_url=info.picture,
        provider="google",
        verified_email=(
            info.email_verified
        ),
    )

    service = OAuthService(
        db
    )

    result = await service.login_google(
        provider_user
    )

    return success_response(
        data=result,
        message="Google login successful",
    )

# =====================================================
# GITHUB LOGIN URL
# =====================================================

@router.get(
    "/github/login",
    status_code=status.HTTP_200_OK,
)
async def github_login(
    request: Request,
):

    github = get_github_provider()

    return await github.authorize_redirect(
        request,
        request.url_for(
            "github_callback"
        ),
    )

# =====================================================
# GITHUB CALLBACK
# =====================================================

@router.get(
    "/github/callback",
    name="github_callback",
)
async def github_callback(
    request: Request,
    db: DatabaseDep,
):

    github = get_github_provider()

    # ==========================================
    # USER CANCELLED AUTHORIZATION
    # ==========================================

    if request.query_params.get(
        "error"
    ):

        return success_response(
            data={
                "success": False,
                "provider": "github",
                "error":
                    request.query_params.get(
                        "error"
                    ),
            },
            message=request.query_params.get(
                "error_description",
                "GitHub authorization cancelled",
            ),
        )

    # ==========================================
    # EXCHANGE CODE FOR TOKEN
    # ==========================================

    try:

        token = await github.authorize_access_token(
            request
        )

    except OAuthError as exc:

        return success_response(
            data={
                "success": False,
                "provider": "github",
            },
            message=str(exc),
        )

    response = await github.get(
        "user",
        token=token,
    )

    user_data = response.json()

    info = GitHubUserInfo.model_validate(
        user_data
    )

    email = info.email

    if not email:

        emails_response = await github.get(
            "user/emails",
            token=token,
        )

        emails = emails_response.json()

        primary = next(
            (
                item
                for item in emails
                if item.get(
                    "primary"
                )
            ),
            None,
        )

        if primary:
            email = primary.get(
                "email"
            )

        if not email:
            raise ValidationError(
                message=(
                    "GitHub account does not provide an email address"
                )
            )

    provider_user = OAuthProviderUser(
        provider_id=str(
            info.id
        ),
        email=email,
        username=info.login,
        display_name=(
            info.name
            or info.login
        ),
        avatar_url=info.avatar_url,
        provider="github",
        verified_email=True,
    )

    service = OAuthService(
        db
    )

    result = await service.login_github(
        provider_user
    )

    return success_response(
        data=result,
        message="GitHub login successful",
    )

# =====================================================
# LINK GOOGLE
# =====================================================

@router.post(
    "/google/link",
    status_code=status.HTTP_200_OK,
)
async def link_google(
    google_id: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = OAuthService(
        db
    )

    result = await service.link_google(
        user_id=current_user.id,
        google_id=google_id,
    )

    return success_response(
        data=result
    )

# =====================================================
# LINK GITHUB
# =====================================================

@router.post(
    "/github/link",
    status_code=status.HTTP_200_OK,
)
async def link_github(
    github_id: str,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = OAuthService(
        db
    )

    result = await service.link_github(
        user_id=current_user.id,
        github_id=github_id,
    )

    return success_response(
        data=result
    )

# =====================================================
# UNLINK GOOGLE
# =====================================================

@router.delete(
    "/google/unlink",
    status_code=status.HTTP_200_OK,
)
async def unlink_google(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = OAuthService(
        db
    )

    result = await service.unlink_google(
        user_id=current_user.id,
    )

    return success_response(
        data=result
    )

# =====================================================
# UNLINK GITHUB
# =====================================================

@router.delete(
    "/github/unlink",
    status_code=status.HTTP_200_OK,
)
async def unlink_github(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = OAuthService(
        db
    )

    result = await service.unlink_github(
        user_id=current_user.id,
    )

    return success_response(
        data=result
    )

# =====================================================
# PROVIDERS
# ====================================================

@router.get(
    "/providers",
    status_code=status.HTTP_200_OK,
)
async def get_providers():

    return success_response(
        data={
            "google_enabled":
                bool(
                    getattr(
                        get_google_provider(),
                        "client_id",
                        None,
                    )
                ),

            "github_enabled":
                bool(
                    getattr(
                        get_github_provider(),
                        "client_id",
                        None,
                    )
                ),
        }
    )
# =====================================================
# LINKED PROVIDERS
# =====================================================

@router.get(
    "/linked-providers",
    status_code=status.HTTP_200_OK,
)
async def get_linked_providers(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = OAuthService(
        db
    )

    result = await service.get_linked_providers(
        user_id=current_user.id,
    )

    return success_response(
        data=result,
    )

# =====================================================
# SET PASSWORD
# =====================================================

@router.post(
    "/set-password",
    status_code=status.HTTP_200_OK,
)
async def set_password(
    payload: PasswordSetupRequest,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = OAuthService(
        db
    )

    result = await service.set_password(
        user_id=current_user.id,
        password=payload.password,
    )

    return success_response(
        data=result,
    )

# =====================================================
# EXPORTS
# =====================================================

__all__ = [
    "router",
]