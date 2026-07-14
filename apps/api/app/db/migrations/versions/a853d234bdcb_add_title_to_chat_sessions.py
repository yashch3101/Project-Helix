"""add title to chat sessions

Revision ID: a853d234bdcb
Revises: b035dc3068b7
Create Date: 2026-07-08 10:20:01.829963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a853d234bdcb'
down_revision: Union[str, Sequence[str], None] = 'b035dc3068b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "chat_sessions",
        sa.Column(
            "title",
            sa.String(),
            nullable=True,
        ),
    )

def downgrade():

    op.drop_column(
        "chat_sessions",
        "title",
    )