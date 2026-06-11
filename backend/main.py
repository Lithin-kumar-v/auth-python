"""
=========================================================
Pageless Gradient API
=========================================================

Main Application Entry Point

Responsibilities
----------------
- FastAPI Bootstrap
- Redis Lifecycle
- Router Registration
- Middleware Registration
- Health Checks
- Readiness Checks
- Exception Handling
- API Information

=========================================================
"""

from __future__ import annotations

import traceback
from uuid import uuid4
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Request,
    Response,
)

from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

import redis.asyncio as redis

# =========================================================
# Config
# =========================================================

from app.core.config import settings

# =========================================================
# Exceptions
# =========================================================

from app.core.exceptions import DomainError

# =========================================================
# middleware
# =========================================================

from starlette.middleware.sessions import SessionMiddleware
# =========================================================
# Database
# =========================================================

from db import REDIS_URL

# =========================================================
# Routers
# =========================================================

from app.auth.routes import router as auth_router
from app.users.routes import router as users_router
from app.sessions.routes import router as sessions_router
from app.oauth.routes import router as oauth_router

# =========================================================
# Globals
# =========================================================

redis_client = None

# =========================================================
# Lifespan
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    global redis_client

    print(
        f"🚀 Starting {settings.APP_NAME}"
    )

    try:

        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True,
        )

        await redis_client.ping()

        app.state.redis = redis_client

        print(
            "✅ Redis Connected"
        )

    except Exception as exc:

        print(
            f"❌ Redis Error: {exc}"
        )

        app.state.redis = None

    yield

    print(
        "🛑 Shutting Down API"
    )

    if redis_client:

        await redis_client.close()

        print(
            "✅ Redis Closed"
        )

# =========================================================
# FastAPI
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    description="""
Pageless Gradient API

Knowledge Operating System

Features

- Authentication
- Topics
- Sessions
- Blocks
- Resources
- Sharing
- AI
- Analytics
""",
)

# =========================================================
# Session Middleware
# =========================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=getattr(
        settings,
        "SECRET_KEY",
        "pageless-gradient-dev-secret-key",
    ),
    same_site="lax",
    https_only=False,
    max_age=86400,
)
# =========================================================
# Middleware
# =========================================================

@app.middleware("http")
async def request_id_middleware(
    request: Request,
    call_next,
):

    request_id = str(uuid4())

    request.state.request_id = (
        request_id
    )

    response: Response = (
        await call_next(request)
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    return response

# =========================================================
# Routers
# =========================================================

app.include_router(
    auth_router,
    prefix="/api/v1",
    tags=["Authentication"],
)
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["Users"],
)
app.include_router(
    sessions_router,
    prefix="/api/v1",
    tags=["Sessions"],
)
app.include_router(
    oauth_router,
    prefix="/api/v1",
    tags=["OAuth"],
)


# =========================================================
# Root
# =========================================================

@app.get(
    "/",
    tags=["System"],
)
async def root():

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "running",
    }

# =========================================================
# API Info
# =========================================================

@app.get(
    "/api-info",
    tags=["System"],
)
async def api_info():

    return {
        "application":
            settings.APP_NAME,

        "version":
            settings.APP_VERSION,

        "environment":
            settings.APP_ENV,

        "features": {
            "auth": True,
            "redis": True,
            "topics": False,
            "sessions": False,
            "blocks": False,
            "sharing": False,
            "ai": False,
        },
    }

# =========================================================
# Health
# =========================================================

@app.get(
    "/health",
    tags=["System"],
)
async def health():

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
    }

# =========================================================
# Ready
# =========================================================

@app.get(
    "/ready",
    tags=["System"],
)
async def ready():

    redis_status = (
        "disconnected"
    )

    try:

        if app.state.redis:

            await app.state.redis.ping()

            redis_status = (
                "connected"
            )

    except Exception:
        pass

    return {
        "ready":
            redis_status
            == "connected",

        "redis":
            redis_status,
    }

# =========================================================
# Cache Test
# =========================================================

@app.get(
    "/api/v1/test/cache",
    tags=["Testing"],
)
async def cache_test():

    if not app.state.redis:

        return {
            "error":
                "Redis unavailable"
        }

    key = "test:cache"

    cached = (
        await app.state.redis.get(
            key
        )
    )

    if cached:

        return {
            "cached": True,
            "value": cached,
        }

    value = (
        datetime.utcnow()
        .isoformat()
    )

    await app.state.redis.set(
        key,
        value,
        ex=300,
    )

    return {
        "cached": False,
        "value": value,
    }

# =========================================================
# No Cache Test
# =========================================================

@app.get(
    "/api/v1/test/no-cache",
    tags=["Testing"],
)
async def no_cache_test():

    return {
        "cached": False,
        "value":
            datetime.utcnow()
            .isoformat(),
    }

# =========================================================
# Domain Errors
# =========================================================

@app.exception_handler(
    DomainError
)
async def domain_error_handler(
    request: Request,
    exc: DomainError,
):

    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )

# =========================================================
# Integrity Errors
# =========================================================

@app.exception_handler(
    IntegrityError
)
async def integrity_error_handler(
    request: Request,
    exc: IntegrityError,
):

    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": {
                "code":
                    "DB_CONSTRAINT_ERROR",
                "message":
                    str(exc.orig),
            },
        },
    )

# =========================================================
# Unknown Errors
# =========================================================

@app.exception_handler(
    Exception
)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
):

    traceback.print_exc()

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code":
                    "INTERNAL_SERVER_ERROR",
                "type":
                    exc.__class__.__name__,
                "message":
                    "Unexpected server error",
            },
        },
    )

from sqlalchemy import text
from db import AsyncSessionFactory


@app.get("/db-test")
async def db_test():

    async with AsyncSessionFactory() as session:

        result = await session.execute(
            text("SELECT 1")
        )

        return {
            "database": result.scalar()
        }
    