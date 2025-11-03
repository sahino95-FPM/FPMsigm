"""Add user table for authentication

Revision ID: 004_add_user
Revises: 003_piece_jointe
Create Date: 2025-11-04 00:05:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_user'
down_revision = '003_piece_jointe'
branch_labels = None
depends_on = None


def upgrade():
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('nom', sa.String(length=100), nullable=False),
        sa.Column('prenom', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=40), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    op.create_index('ix_user_role', 'user', ['role'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_user_role', table_name='user')
    op.drop_index('ix_user_email', table_name='user')

    # Drop table
    op.drop_table('user')
