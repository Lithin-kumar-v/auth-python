from __future__ import annotations

import os
from typing import AsyncGenerator, Generator, Optional

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from redis.asyncio import Redis

# =========================================================
# Load Environment
# =========================================================

load_dotenv()

# =========================================================
# Environment Variables
# =========================================================

DATABASE_URL = os.getenv("DATABASE_URL")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")

REDIS_URL = os.getenv("REDIS_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

if not SYNC_DATABASE_URL:
    raise RuntimeError("SYNC_DATABASE_URL is not configured")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not configured")

# =========================================================
# Base Model
# =========================================================

Base = declarative_base()

# =========================================================
# Sync Engine
# Used For:
# - Alembic
# - Scripts
# - Admin Utilities
# =========================================================

SYNC_ENGINE = create_engine(
    SYNC_DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SyncSessionFactory = sessionmaker(
    bind=SYNC_ENGINE,
    autoflush=False,
    autocommit=False,
    class_=Session,
)

# =========================================================
# Async Engine
# Used For:
# - FastAPI Runtime
# - Services
# - Repositories
# =========================================================

ASYNC_ENGINE = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

AsyncSessionFactory = async_sessionmaker(
    bind=ASYNC_ENGINE,
    expire_on_commit=False,
)

# =========================================================
# Sync Session Dependency
# =========================================================

def get_db() -> Generator[Session, None, None]:
    db = SyncSessionFactory()

    try:
        yield db

    finally:
        db.close()

# =========================================================
# Async Session Dependency
# =========================================================

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session

# =========================================================
# Redis
# =========================================================

redis_client: Optional[Redis] = None

async def get_redis() -> Optional[Redis]:
    return redis_client

# =========================================================
# Health Helpers
# =========================================================

async def check_database() -> bool:
    try:
        async with ASYNC_ENGINE.begin() as conn:
            await conn.run_sync(lambda _: None)

        return True

    except Exception:
        return False


async def check_redis() -> bool:
    try:
        if not redis_client:
            return False

        await redis_client.ping()

        return True

    except Exception:
        return False

# =========================================================
# Compatibility Aliases
# =========================================================

get_session = get_db
get_sync_session = get_db