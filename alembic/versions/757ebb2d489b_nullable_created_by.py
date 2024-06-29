"""nullable created_by

Revision ID: 757ebb2d489b
Revises: 56f3fc7f1ed2
Create Date: 2024-06-29 17:31:30.153389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '757ebb2d489b'
down_revision: Union[str, None] = '56f3fc7f1ed2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('file', 'created_by',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('file', 'created_by',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
