"""create highlight model

Revision ID: f3fa8de8c800
Revises: d025c2ce3fef
Create Date: 2024-10-24 15:02:24.119926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3fa8de8c800'
down_revision: Union[str, None] = 'd025c2ce3fef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('highlights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('chapter', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_highlights_id'), 'highlights', ['id'], unique=False)
    op.create_index(op.f('ix_highlights_title'), 'highlights', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_highlights_title'), table_name='highlights')
    op.drop_index(op.f('ix_highlights_id'), table_name='highlights')
    op.drop_table('highlights')
    # ### end Alembic commands ###
