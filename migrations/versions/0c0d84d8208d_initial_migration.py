"""Initial migration

Revision ID: 0c0d84d8208d
Revises: 
Create Date: 2021-03-13 16:26:54.586050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c0d84d8208d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    op.create_table('store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_store_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_store'))
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=120), nullable=False),
    sa.Column('price_cents', sa.Integer(), nullable=True),
    sa.Column('picture_url', sa.Text(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], name=op.f('fk_product_creator_id_user')),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], name=op.f('fk_product_store_id_store')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_product'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('store')
    op.drop_table('user')
    # ### end Alembic commands ###