"""add updated_at to users

Revision ID: 14c59be991a5
Revises: 6620ebaf1dc1
Create Date: 2026-11-04 11:10:18.763253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14c59be991a5'
down_revision: Union[str, Sequence[str], None] = '6620ebaf1dc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('(CURRENT_TIMESTAMP)'),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'updated_at')
