"""Initial migration

Revision ID: 77330d8e2381
Revises: 
Create Date: 2024-08-28 11:30:04.055168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77330d8e2381'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('priority', sa.String(length=20), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('priority')

    # ### end Alembic commands ###
