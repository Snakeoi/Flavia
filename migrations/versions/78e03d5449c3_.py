"""empty message

Revision ID: 78e03d5449c3
Revises: 04ed2e132a62
Create Date: 2025-01-29 22:30:52.782590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78e03d5449c3'
down_revision = '04ed2e132a62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agreements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('agreements')
    # ### end Alembic commands ###
