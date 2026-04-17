"""seed parcel types

Revision ID: b7507cc2af54
Revises: 15de663f3729
Create Date: 2026-04-17 11:56:12.910833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7507cc2af54'
down_revision: Union[str, Sequence[str], None] = '15de663f3729'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        INSERT INTO parcel_types (name)
        VALUES
            ('одежда'),
            ('электроника'),
            ('разное');
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM parcel_types
        WHERE name IN ('одежда', 'электроника', 'разное');
        """
    )
