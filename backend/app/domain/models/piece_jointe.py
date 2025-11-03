from datetime import datetime
from app.extensions import db


class PieceJointe(db.Model):
    """Gestion des pièces jointes pour les dossiers CREDEF"""
    __tablename__ = "piece_jointe"

    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('credef_dossier.id'), nullable=False, index=True)
    type_piece = db.Column(db.String(50), nullable=False, index=True)  # CNI, BULLETIN_PAIE, etc.
    nom_fichier = db.Column(db.String(255), nullable=False)
    chemin_stockage = db.Column(db.String(500), nullable=False)
    taille_octets = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=True)
    est_obligatoire = db.Column(db.Boolean, default=False)
    est_valide = db.Column(db.Boolean, default=False)
    uploaded_by = db.Column(db.Integer, nullable=True)  # ID de l'acteur qui a uploadé
    commentaire = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relation avec le dossier
    dossier = db.relationship('CredefDossier', backref='pieces_jointes', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "dossier_id": self.dossier_id,
            "type_piece": self.type_piece,
            "nom_fichier": self.nom_fichier,
            "taille_octets": self.taille_octets,
            "mime_type": self.mime_type,
            "est_obligatoire": self.est_obligatoire,
            "est_valide": self.est_valide,
            "uploaded_by": self.uploaded_by,
            "commentaire": self.commentaire,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
