"""Initial migration - create credef_dossier table

Revision ID: 001_initial
Revises:
Create Date: 2025-11-03 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create credef_dossier table
    op.create_table(
        'credef_dossier',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ref', sa.String(length=32), nullable=False),
        sa.Column('adherent_id', sa.Integer(), nullable=True),
        sa.Column('date_depot', sa.Date(), nullable=True),
        sa.Column('montant_demande', sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column('montant_accorde', sa.Numeric(precision=14, scale=2), nullable=True),
        sa.Column('taux', sa.Numeric(precision=5, scale=2), server_default='10', nullable=True),
        sa.Column('duree_mois', sa.Integer(), nullable=True),
        sa.Column('statut', sa.String(length=40), server_default='BROUILLON', nullable=True),
        sa.Column('mois_traitement', sa.String(length=7), nullable=True),
        sa.Column('acteur_courant_id', sa.Integer(), nullable=True),
        sa.Column('commentaire_rejet', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_credef_dossier_ref', 'credef_dossier', ['ref'], unique=True)
    op.create_index('ix_credef_dossier_statut', 'credef_dossier', ['statut'], unique=False)
    op.create_index('ix_credef_dossier_mois_traitement', 'credef_dossier', ['mois_traitement'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_credef_dossier_mois_traitement', table_name='credef_dossier')
    op.drop_index('ix_credef_dossier_statut', table_name='credef_dossier')
    op.drop_index('ix_credef_dossier_ref', table_name='credef_dossier')

    # Drop table
    op.drop_table('credef_dossier')
