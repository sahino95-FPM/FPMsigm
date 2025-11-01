from app.extensions import db


class CredefDossier(db.Model):
    __tablename__ = "credef_dossier"

    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(32), unique=True, index=True, nullable=False)
    adherent_id = db.Column(db.Integer, nullable=True)
    date_depot = db.Column(db.Date, nullable=True)
    montant_demande = db.Column(db.Numeric(14, 2), nullable=True)
    montant_accorde = db.Column(db.Numeric(14, 2), nullable=True)
    taux = db.Column(db.Numeric(5, 2), default=10)
    duree_mois = db.Column(db.Integer)
    statut = db.Column(db.String(40), default="BROUILLON", index=True)
    mois_traitement = db.Column(db.String(7), index=True)  # "YYYY-MM"
    acteur_courant_id = db.Column(db.Integer)
    commentaire_rejet = db.Column(db.Text)
