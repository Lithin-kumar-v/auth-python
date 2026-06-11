from __future__ import annotations

import uuid

from datetime import datetime
from datetime import timezone

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db import Base


# =========================================================
# Helpers
# =========================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# =========================================================
# Users
# =========================================================

class User(Base):

    __tablename__ = "users"

    __table_args__ = (

        Index(
            "idx_users_created_at",
            "created_at",
        ),

        Index(
            "idx_users_last_login_at",
            "last_login_at",
        ),

        Index(
            "idx_users_active_verified",
            "is_active",
            "is_verified",
        ),

        Index(
            "idx_users_auth_provider",
            "auth_provider",
        ),

        Index(
            "idx_users_google_id",
            "google_id",
        ),

        Index(
            "idx_users_github_id",
            "github_id",
        ),

    )

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # =====================================================
    # Identity
    # =====================================================

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    # =====================================================
    # Authentication
    # =====================================================

    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    google_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    github_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    auth_provider: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="password",
        server_default="password",
    )

    # =====================================================
    # Status
    # =====================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    # =====================================================
    # Timestamps
    # =====================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    profile: Mapped["UserProfile"] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (
            f"<User("
            f"id={self.id}, "
            f"email='{self.email}'"
            f")>"
        )


# =========================================================
# User Profiles
# =========================================================

class UserProfile(Base):

    __tablename__ = "user_profiles"

    __table_args__ = (

        Index(
            "idx_user_profiles_display_name",
            "display_name",
        ),

        Index(
            "idx_user_profiles_language",
            "language",
        ),

        Index(
            "idx_user_profiles_timezone",
            "timezone",
        ),

    )

    # =====================================================
    # Primary Key
    # =====================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # =====================================================
    # Foreign Key
    # =====================================================

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    # =====================================================
    # Profile Data
    # =====================================================

    display_name: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="UTC",
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="en",
    )

    # =====================================================
    # Timestamps
    # =====================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )

    # =====================================================
    # Relationships
    # =====================================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="profile",
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (
            f"<UserProfile("
            f"user_id={self.user_id}"
            f")>"
        )