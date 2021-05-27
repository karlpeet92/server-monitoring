"""Add response_time column

Revision ID: d8a526a1970c
Revises: ae4f79955418
Create Date: 2020-08-12 10:35:08.675630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8a526a1970c'
down_revision = 'ae4f79955418'
branch_labels = None
depends_on = None


def upgrade():
   op.add_column('site', sa.Column('response_time', sa.Float))


def downgrade():
    op.drop_column('site', 'response_time')
