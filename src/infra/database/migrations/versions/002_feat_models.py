"""feat: models

Revision ID: c9f6c36c85c5
Revises: 5c7b5713b6d5
Create Date: 2025-12-12 19:21:36.142500

"""
from alembic import op
import sqlalchemy as sa


revision= 'c9f6c36c85c5'
down_revision = '5c7b5713b6d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('cats',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('years_of_experience', sa.Integer(), nullable=True),
    sa.Column('breed', sa.String(), nullable=True),
    sa.Column('salary', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cats_id'), 'cats', ['id'], unique=False)
    op.create_table('missions',
    sa.Column('cat_id', sa.Integer(), nullable=True),
    sa.Column('is_completed', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['cat_id'], ['cats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_missions_id'), 'missions', ['id'], unique=False)
    op.create_table('targets',
    sa.Column('mission_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('is_completed', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_targets_id'), 'targets', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_targets_id'), table_name='targets')
    op.drop_table('targets')
    op.drop_index(op.f('ix_missions_id'), table_name='missions')
    op.drop_table('missions')
    op.drop_index(op.f('ix_cats_id'), table_name='cats')
    op.drop_table('cats')
