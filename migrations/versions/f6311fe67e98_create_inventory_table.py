"""Create inventory table

Revision ID: f6311fe67e98
Revises: ec9d5fe5804f
Create Date: 2024-06-17 22:31:54.359933

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f6311fe67e98"
down_revision: Union[str, None] = "ec9d5fe5804f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("book_id", sa.String, sa.ForeignKey("Book.isbn"), unique=True),
        sa.Column("count", sa.Integer),
        sa.Column("borrowed_count", sa.Integer),
    )


def downgrade() -> None:
    op.drop_table("inventory")
