"""add_oauth_fields_to_users

Revision ID: a8d905b274b2
Revises: ac0c0eaa9f0c
Create Date: 2026-06-09 12:30:14.720067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d905b274b2'
down_revision: Union[str, None] = 'ac0c0eaa9f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "users",
        sa.Column(
            "google_id",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "github_id",
            sa.String(length=255),
            nullable=True,
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "auth_provider",
            sa.String(length=50),
            nullable=False,
            server_default="password",
        ),
    )

    op.create_unique_constraint(
        "uq_users_google_id",
        "users",
        ["google_id"],
    )

    op.create_unique_constraint(
        "uq_users_github_id",
        "users",
        ["github_id"],
    )

    op.create_index(
        "idx_users_auth_provider",
        "users",
        ["auth_provider"],
    )


def downgrade():

    op.drop_index(
        "idx_users_auth_provider",
        table_name="users",
    )

    op.drop_constraint(
        "uq_users_google_id",
        "users",
        type_="unique",
    )

    op.drop_constraint(
        "uq_users_github_id",
        "users",
        type_="unique",
    )

    op.drop_column(
        "users",
        "google_id",
    )

    op.drop_column(
        "users",
        "github_id",
    )

    op.drop_column(
        "users",
        "auth_provider",
    )