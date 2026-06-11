"""user rebuild

Revision ID: e1271ec828ad
Revises: a8d905b274b2
Create Date: 2026-06-09 15:02:09.416830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e1271ec828ad'
down_revision: Union[str, None] = 'a8d905b274b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from sqlalchemy import inspect


def table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = inspect(bind)

    return table_name in inspector.get_table_names()


def column_exists(
    table_name: str,
    column_name: str,
) -> bool:

    bind = op.get_bind()
    inspector = inspect(bind)

    columns = inspector.get_columns(table_name)

    return any(
        col["name"] == column_name
        for col in columns
    )


def index_exists(
    table_name: str,
    index_name: str,
) -> bool:

    bind = op.get_bind()
    inspector = inspect(bind)

    indexes = inspector.get_indexes(table_name)

    return any(
        idx["name"] == index_name
        for idx in indexes
    )

def upgrade():

    # =====================================================
    # USERS
    # =====================================================

    if not table_exists("users"):

        op.create_table(
            "users",

            sa.Column(
                "id",
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
            ),

            sa.Column(
                "email",
                sa.String(255),
                nullable=False,
                unique=True,
            ),

            sa.Column(
                "username",
                sa.String(50),
                nullable=False,
                unique=True,
            ),

            sa.Column(
                "password_hash",
                sa.String(255),
                nullable=True,
            ),

            sa.Column(
                "google_id",
                sa.String(255),
                nullable=True,
                unique=True,
            ),

            sa.Column(
                "github_id",
                sa.String(255),
                nullable=True,
                unique=True,
            ),

            sa.Column(
                "auth_provider",
                sa.String(20),
                nullable=False,
                server_default="password",
            ),

            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default="true",
            ),

            sa.Column(
                "is_verified",
                sa.Boolean(),
                nullable=False,
                server_default="false",
            ),

            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
            ),

            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
            ),

            sa.Column(
                "last_login_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
        )

    else:

        if not column_exists("users", "google_id"):

            op.add_column(
                "users",
                sa.Column(
                    "google_id",
                    sa.String(255),
                    nullable=True,
                ),
            )

        if not column_exists("users", "github_id"):

            op.add_column(
                "users",
                sa.Column(
                    "github_id",
                    sa.String(255),
                    nullable=True,
                ),
            )

        if not column_exists("users", "auth_provider"):

            op.add_column(
                "users",
                sa.Column(
                    "auth_provider",
                    sa.String(20),
                    nullable=False,
                    server_default="password",
                ),
            )

        # =====================================================
    # USER PROFILES
    # =====================================================

    if not table_exists("user_profiles"):

        op.create_table(
            "user_profiles",

            sa.Column(
                "id",
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False,
            ),

            sa.Column(
                "user_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey(
                    "users.id",
                    ondelete="CASCADE",
                ),
                nullable=False,
                unique=True,
            ),

            sa.Column(
                "display_name",
                sa.String(120),
                nullable=True,
            ),

            sa.Column(
                "avatar_url",
                sa.String(1000),
                nullable=True,
            ),

            sa.Column(
                "bio",
                sa.Text(),
                nullable=True,
            ),

            sa.Column(
                "timezone",
                sa.String(100),
                nullable=False,
                server_default="UTC",
            ),

            sa.Column(
                "language",
                sa.String(20),
                nullable=False,
                server_default="en",
            ),

            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
            ),

            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
            ),
        )

    # =====================================================
    # USERS INDEXES
    # =====================================================

    user_indexes = [

        ("idx_users_created_at", ["created_at"]),

        ("idx_users_last_login_at", ["last_login_at"]),

        (
            "idx_users_active_verified",
            ["is_active", "is_verified"],
        ),

        ("idx_users_auth_provider", ["auth_provider"]),

        ("idx_users_google_id", ["google_id"]),

        ("idx_users_github_id", ["github_id"]),
    ]

    for index_name, columns in user_indexes:

        if not index_exists(
            "users",
            index_name,
        ):

            op.create_index(
                index_name,
                "users",
                columns,
            )

    # =====================================================
    # PROFILE INDEXES
    # =====================================================

    profile_indexes = [

        (
            "idx_user_profiles_display_name",
            ["display_name"],
        ),

        (
            "idx_user_profiles_language",
            ["language"],
        ),

        (
            "idx_user_profiles_timezone",
            ["timezone"],
        ),
    ]

    for index_name, columns in profile_indexes:

        if not index_exists(
            "user_profiles",
            index_name,
        ):

            op.create_index(
                index_name,
                "user_profiles",
                columns,
            )

def downgrade():

    bind = op.get_bind()

    inspector = sa.inspect(bind)

    if "user_profiles" in inspector.get_table_names():

        op.drop_table("user_profiles")

    if "users" in inspector.get_table_names():

        op.drop_table("users")