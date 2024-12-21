"""empty message

Revision ID: 04ed2e132a62
Revises: 02ee289773de
Create Date: 2024-10-15 22:47:56.086289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '04ed2e132a62'
down_revision = '02ee289773de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)

    # ### end Alembic commands ###