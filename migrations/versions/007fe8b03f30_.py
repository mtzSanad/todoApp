"""empty message

Revision ID: 007fe8b03f30
Revises: 8aa25429c5e7
Create Date: 2020-11-14 07:41:11.308372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007fe8b03f30'
down_revision = '8aa25429c5e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('list_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'todolists', ['list_id'], ['id'])

    op.execute("INSERT INTO TODOLISTS (NAME) VALUES ('UNCATEGORIZED');")
    op.execute("UPDATE TODOS SET LIST_ID = 1;")

    op.alter_column('todos', 'list_id', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'list_id')
    op.drop_table('todolists')
    # ### end Alembic commands ###
