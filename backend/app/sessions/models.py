from __future__ import annotations

import uuid

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db import Base


class UserSession(Base):

    __tablename__ = "user_sessions"

    # ==================================================
    # Indexes
    # ==================================================

    __table_args__ = (

        Index(
            "ix_sessions_user_revoked",
            "user_id",
            "revoked",
        ),

        Index(
            "ix_sessions_user_last_activity",
            "user_id",
            "last_activity",
        ),

        Index(
            "ix_sessions_user_expires",
            "user_id",
            "expires_at",
        ),

        Index(
            "ix_sessions_country",
            "country",
        ),

        Index(
            "ix_sessions_login_method",
            "login_method",
        ),

        Index(
            "ix_sessions_suspicious",
            "suspicious",
        ),

    )

    # ==================================================
    # Primary Key
    # ==================================================

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # ==================================================
    # User Relationship
    # ==================================================

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ==================================================
    # Token Security
    # ==================================================

    refresh_token_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    token_family: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    replaced_by_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==================================================
    # Session Metadata
    # ==================================================

    session_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    login_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="password",
        server_default="password",
    )

    # ==================================================
    # Device Metadata
    # ==================================================

    device_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    device_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    browser: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    browser_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    os: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    os_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ==================================================
    # Network Metadata
    # ==================================================

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    timezone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    # ==================================================
    # Activity Tracking
    # ==================================================

    login_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # ==================================================
    # Security Flags
    # ==================================================

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    revoked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    revoked_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    suspicious: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    # ==================================================
    # Audit Fields
    # ==================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ==================================================
    # Relationships
    # ==================================================

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions",
    )

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self) -> str:
        return (
            f"<UserSession("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"revoked={self.revoked}"
            f")>"
        )