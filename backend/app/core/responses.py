"""
=========================================================
Pageless Gradient
Enterprise API Response System
=========================================================

Features
--------
✓ Standard Success Responses
✓ Standard Error Responses
✓ Pagination Responses
✓ Validation Responses
✓ Metadata Support
✓ Request Tracking
✓ Timestamp Support
✓ Consistent API Contract

=========================================================
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


# =========================================================
# Helpers
# =========================================================

def utc_timestamp() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def request_id() -> str:
    return str(uuid4())


# =========================================================
# Success Response
# =========================================================

def success_response(
    data: Any = None,
    message: str = "Success",
    meta: dict | None = None,
):
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta or {},
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Created Response
# =========================================================

def created_response(
    data: Any = None,
    message: str = "Created successfully",
):
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Error Response
# =========================================================

def error_response(
    message: str,
    code: str = "ERROR",
    details: Any = None,
):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Validation Error Response
# =========================================================

def validation_error_response(
    errors: list[dict],
):
    return {
        "success": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Validation failed",
            "details": errors,
        },
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Pagination Response
# =========================================================

def paginated_response(
    *,
    items: list[Any],
    page: int,
    limit: int,
    total: int,
):
    pages = (
        (total + limit - 1) // limit
        if limit > 0
        else 1
    )

    return {
        "success": True,
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "has_next": page < pages,
            "has_previous": page > 1,
        },
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Empty Response
# =========================================================

def empty_response(
    message: str = "No content",
):
    return {
        "success": True,
        "message": message,
        "data": None,
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Health Response
# =========================================================

def health_response(
    *,
    service: str,
    status: str,
    version: str,
    checks: dict | None = None,
):
    return {
        "service": service,
        "status": status,
        "version": version,
        "checks": checks or {},
        "timestamp": utc_timestamp(),
    }


# =========================================================
# Auth Response
# =========================================================

def auth_response(
    *,
    access_token: str,
    refresh_token: str,
    user: dict,
):
    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "user": user,
        },
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Resource Response
# =========================================================

def resource_response(
    *,
    resource: Any,
):
    return {
        "success": True,
        "data": resource,
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }


# =========================================================
# Collection Response
# =========================================================

def collection_response(
    *,
    items: list[Any],
):
    return {
        "success": True,
        "count": len(items),
        "data": items,
        "timestamp": utc_timestamp(),
        "request_id": request_id(),
    }