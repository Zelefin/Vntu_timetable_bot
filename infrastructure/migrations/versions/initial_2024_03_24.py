"""1_0_0

Revision ID: 9731ec95cf9b
Revises: 
Create Date: 2024-04-25 22:10:37.128301

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "9731ec95cf9b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("user_id", sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column("username", sa.String(length=128), nullable=True),
        sa.Column("full_name", sa.String(length=128), nullable=False),
        sa.Column("faculty_id", sa.Integer(), nullable=True),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("subgroup", sa.Integer(), nullable=True),
        sa.Column("group_name", sa.String(), nullable=True),
        sa.Column(
            "active", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
