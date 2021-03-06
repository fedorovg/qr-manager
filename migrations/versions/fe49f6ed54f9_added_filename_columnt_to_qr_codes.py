"""Added filename columnt to QR codes

Revision ID: fe49f6ed54f9
Revises: 34691a3b8128
Create Date: 2021-10-03 22:09:33.667914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe49f6ed54f9'
down_revision = '34691a3b8128'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('qr_code', sa.Column('stored_name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('qr_code', 'stored_name')
    # ### end Alembic commands ###
