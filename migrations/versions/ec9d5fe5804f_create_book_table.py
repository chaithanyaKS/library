"""Create book table

Revision ID: ec9d5fe5804f
Revises: bd1e2c5bfc6a
Create Date: 2024-06-17 22:26:23.436551

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ec9d5fe5804f"
down_revision: Union[str, None] = "bd1e2c5bfc6a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "book",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("isbn", sa.String),
        sa.Column("title", sa.String),
        sa.Column("author", sa.String()),
        sa.Column("subject", sa.String()),
    )


def downgrade() -> None:
    op.drop_table("book")
