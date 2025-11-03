"""Add piece_jointe table for file attachments

Revision ID: 003_piece_jointe
Revises: 002_workflow_log
Create Date: 2025-11-03 23:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_piece_jointe'
down_revision = '002_workflow_log'
branch_labels = None
depends_on = None


def upgrade():
    # Create piece_jointe table
    op.create_table(
        'piece_jointe',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dossier_id', sa.Integer(), nullable=False),
        sa.Column('type_piece', sa.String(length=50), nullable=False),
        sa.Column('nom_fichier', sa.String(length=255), nullable=False),
        sa.Column('chemin_stockage', sa.String(length=500), nullable=False),
        sa.Column('taille_octets', sa.Integer(), nullable=False),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('est_obligatoire', sa.Boolean(), server_default='0', nullable=True),
        sa.Column('est_valide', sa.Boolean(), server_default='0', nullable=True),
        sa.Column('uploaded_by', sa.Integer(), nullable=True),
        sa.Column('commentaire', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['dossier_id'], ['credef_dossier.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_piece_jointe_dossier_id', 'piece_jointe', ['dossier_id'], unique=False)
    op.create_index('ix_piece_jointe_type_piece', 'piece_jointe', ['type_piece'], unique=False)
    op.create_index('ix_piece_jointe_created_at', 'piece_jointe', ['created_at'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_piece_jointe_created_at', table_name='piece_jointe')
    op.drop_index('ix_piece_jointe_type_piece', table_name='piece_jointe')
    op.drop_index('ix_piece_jointe_dossier_id', table_name='piece_jointe')

    # Drop table
    op.drop_table('piece_jointe')
