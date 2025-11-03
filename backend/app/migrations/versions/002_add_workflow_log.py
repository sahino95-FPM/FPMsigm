"""Add workflow_log table for audit trail

Revision ID: 002_workflow_log
Revises: 001_initial
Create Date: 2025-11-03 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_workflow_log'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Create workflow_log table
    op.create_table(
        'workflow_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dossier_id', sa.Integer(), nullable=False),
        sa.Column('statut_from', sa.String(length=40), nullable=True),
        sa.Column('statut_to', sa.String(length=40), nullable=False),
        sa.Column('acteur_id', sa.Integer(), nullable=True),
        sa.Column('role', sa.String(length=40), nullable=True),
        sa.Column('commentaire', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['dossier_id'], ['credef_dossier.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_workflow_log_dossier_id', 'workflow_log', ['dossier_id'], unique=False)
    op.create_index('ix_workflow_log_created_at', 'workflow_log', ['created_at'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_workflow_log_created_at', table_name='workflow_log')
    op.drop_index('ix_workflow_log_dossier_id', table_name='workflow_log')

    # Drop table
    op.drop_table('workflow_log')
