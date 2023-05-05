"""empty message

Revision ID: 29327710a74b
Revises: e5ba4a74bb0c
Create Date: 2023-05-05 10:29:32.596158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29327710a74b'
down_revision = 'e5ba4a74bb0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=128), nullable=True))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer_data', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=128), nullable=True))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###