from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from app.common.dependencies import (
    DatabaseDep,
    CurrentUserDep,
)

from app.core.responses import (
    success_response,
)

from app.sessions.service import (
    SessionService,
)

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)

# =========================================================
# LIST USER SESSIONS
# =========================================================

@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_sessions(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    sessions = await service.list_sessions(
        current_user.id,
    )

    return success_response(
        data=sessions,
    )


# =========================================================
# CURRENT SESSION
# MUST STAY ABOVE /{session_id}
# =========================================================

@router.get(
    "/current",
    status_code=status.HTTP_200_OK,
)
async def get_current_session(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    session = await service.get_current_session(
        current_user.id,
    )

    return success_response(
        data=session,
    )


# =========================================================
# SESSION STATS
# MUST STAY ABOVE /{session_id}
# =========================================================

@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
)
async def get_session_stats(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    stats = await service.get_stats(
        current_user.id,
    )

    return success_response(
        data=stats,
    )


# =========================================================
# LOGOUT ALL DEVICES
# MUST STAY ABOVE /{session_id}
# =========================================================

@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
)
async def logout_all_devices(
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    result = await service.logout_all_devices(
        current_user.id,
    )

    return success_response(
        data=result,
        message="All devices logged out",
    )


# =========================================================
# CLEANUP EXPIRED
# MUST STAY ABOVE /{session_id}
# =========================================================

@router.post(
    "/cleanup",
    status_code=status.HTTP_200_OK,
)
async def cleanup_expired_sessions(
    db: DatabaseDep,
):

    service = SessionService(db)

    result = await service.cleanup_expired_sessions()

    return success_response(
        data=result,
        message="Expired sessions cleaned",
    )


# =========================================================
# GET SESSION
# KEEP BELOW STATIC ROUTES
# =========================================================

@router.get(
    "/{session_id}",
    status_code=status.HTTP_200_OK,
)
async def get_session(
    session_id: UUID,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    session = await service.get_session(
        session_id,
    )

    if not session:

        return success_response(
            data=None,
            message="Session not found",
        )

    if session.user_id != current_user.id:

        return success_response(
            data=None,
            message="Access denied",
        )

    return success_response(
        data=session,
    )


# =========================================================
# LOGOUT DEVICE
# KEEP BELOW STATIC ROUTES
# =========================================================

@router.delete(
    "/{session_id}",
    status_code=status.HTTP_200_OK,
)
async def logout_device(
    session_id: UUID,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    result = await service.logout_device(
        user_id=current_user.id,
        session_id=session_id,
    )

    return success_response(
        data=result,
        message="Device logged out",
    )


# =========================================================
# MARK SUSPICIOUS
# KEEP BELOW STATIC ROUTES
# =========================================================

@router.post(
    "/{session_id}/suspicious",
    status_code=status.HTTP_200_OK,
)
async def mark_suspicious(
    session_id: UUID,
    db: DatabaseDep,
    current_user: CurrentUserDep,
):

    service = SessionService(db)

    session = await service.get_session(
        session_id,
    )

    if not session:

        return success_response(
            data=None,
            message="Session not found",
        )

    if session.user_id != current_user.id:

        return success_response(
            data=None,
            message="Access denied",
        )

    result = await service.mark_suspicious(
        session_id,
    )

    return success_response(
        data=result,
        message="Session marked suspicious",
    )