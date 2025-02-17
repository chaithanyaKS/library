"""create borrowing table

Revision ID: 0e0da6075e7e
Revises: f6311fe67e98
Create Date: 2024-06-19 15:53:05.224832

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0e0da6075e7e"
down_revision: Union[str, None] = "f6311fe67e98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "borrowing",
        sa.Column("id", sa.INTEGER, nullable=False, primary_key=True),
        sa.Column("inventory_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.UniqueConstraint(
            "inventory_id", "user_id", name="uniq_inventory_id_user_id"
        ),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("borrowing")
