"""Create user table

Revision ID: bd1e2c5bfc6a
Revises:
Create Date: 2024-06-17 22:20:25.381040

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bd1e2c5bfc6a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_account",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True),
        sa.Column("password", sa.String(256)),
        sa.Column("name", sa.String(50)),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table("user_account")
