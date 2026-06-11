"""sesson creation

Revision ID: 25d2e91c17d6
Revises: e1271ec828ad
Create Date: 2026-06-09 15:07:00.834864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '25d2e91c17d6'
down_revision: Union[str, None] = 'e1271ec828ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = inspect(bind)

    return table_name in inspector.get_table_names()


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

    if not table_exists("user_sessions"):

        op.create_table(

            "user_sessions",

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
            ),

            sa.Column(
                "refresh_token_hash",
                sa.Text(),
                nullable=False,
                unique=True,
            ),

            sa.Column(
                "token_family",
                sa.String(255),
                nullable=True,
            ),

            sa.Column(
                "replaced_by_token",
                sa.Text(),
                nullable=True,
            ),

            sa.Column(
                "session_name",
                sa.String(255),
                nullable=True,
            ),

            sa.Column(
                "login_method",
                sa.String(50),
                nullable=False,
                server_default="password",
            ),

            sa.Column(
                "device_name",
                sa.String(255),
                nullable=True,
            ),

            sa.Column(
                "device_type",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "browser",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "browser_version",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "os",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "os_version",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "user_agent",
                sa.Text(),
                nullable=True,
            ),

            sa.Column(
                "ip_address",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "country",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "region",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "city",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "timezone",
                sa.String(100),
                nullable=True,
            ),

            sa.Column(
                "login_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),

            sa.Column(
                "last_activity",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),

            sa.Column(
                "expires_at",
                sa.DateTime(timezone=True),
                nullable=False,
            ),

            sa.Column(
                "is_current",
                sa.Boolean(),
                nullable=False,
                server_default="false",
            ),

            sa.Column(
                "revoked",
                sa.Boolean(),
                nullable=False,
                server_default="false",
            ),

            sa.Column(
                "revoked_reason",
                sa.String(255),
                nullable=True,
            ),

            sa.Column(
                "revoked_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),

            sa.Column(
                "suspicious",
                sa.Boolean(),
                nullable=False,
                server_default="false",
            ),

            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),

            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                nullable=False,
                server_default=sa.func.now(),
            ),
        )

    indexes = [

        (
            "ix_sessions_user_revoked",
            ["user_id", "revoked"],
        ),

        (
            "ix_sessions_user_last_activity",
            ["user_id", "last_activity"],
        ),

        (
            "ix_sessions_user_expires",
            ["user_id", "expires_at"],
        ),

        (
            "ix_sessions_country",
            ["country"],
        ),

        (
            "ix_sessions_login_method",
            ["login_method"],
        ),

        (
            "ix_sessions_suspicious",
            ["suspicious"],
        ),

        (
            "ix_user_sessions_token_family",
            ["token_family"],
        ),

        (
            "ix_user_sessions_expires_at",
            ["expires_at"],
        ),

        (
            "ix_user_sessions_user_id",
            ["user_id"],
        ),
    ]

    for index_name, columns in indexes:

        if not index_exists(
            "user_sessions",
            index_name,
        ):

            op.create_index(
                index_name,
                "user_sessions",
                columns,
            )


def downgrade():

    bind = op.get_bind()

    inspector = sa.inspect(bind)

    if "user_sessions" in inspector.get_table_names():

        op.drop_table("user_sessions")