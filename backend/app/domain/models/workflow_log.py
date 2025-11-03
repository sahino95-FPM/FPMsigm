from datetime import datetime
from app.extensions import db


class WorkflowLog(db.Model):
    """Log des transitions de workflow pour traçabilité et audit"""
    __tablename__ = "workflow_log"

    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('credef_dossier.id'), nullable=False, index=True)
    statut_from = db.Column(db.String(40), nullable=True)  # null si création
    statut_to = db.Column(db.String(40), nullable=False)
    acteur_id = db.Column(db.Integer, nullable=True)
    role = db.Column(db.String(40), nullable=True)
    commentaire = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relation avec le dossier
    dossier = db.relationship('CredefDossier', backref='workflow_logs', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "dossier_id": self.dossier_id,
            "statut_from": self.statut_from,
            "statut_to": self.statut_to,
            "acteur_id": self.acteur_id,
            "role": self.role,
            "commentaire": self.commentaire,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
