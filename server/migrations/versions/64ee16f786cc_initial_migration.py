"""Initial migration

Revision ID: 64ee16f786cc
Revises: 
Create Date: 2023-11-20 23:17:53.162475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64ee16f786cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('founding_year', sa.Integer(), nullable=True),
    sa.Column('region', sa.String(length=255), nullable=True),
    sa.Column('operation_size', sa.String(length=20), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cheeses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.String(length=255), nullable=True),
    sa.Column('producer_id', sa.Integer(), nullable=True),
    sa.Column('is_raw_milk', sa.Boolean(), nullable=True),
    sa.Column('production_date', sa.DateTime(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['producer_id'], ['producers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cheeses')
    op.drop_table('producers')
    # ### end Alembic commands ###