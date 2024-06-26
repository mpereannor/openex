"""empty message

Revision ID: d9a654d44dba
Revises: 
Create Date: 2024-04-25 23:54:09.833419

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a654d44dba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=64),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=64),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=64),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(length=64),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
