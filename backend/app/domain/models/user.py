from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    """Modèle utilisateur avec authentification et rôles"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), nullable=False, index=True)  # ADMIN, SACV, DCFF, DCPRE, DTR, ADHERENT
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def set_password(self, password):
        """Hash et stocke le mot de passe"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_sensitive=False):
        """Convertit l'utilisateur en dictionnaire"""
        data = {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "prenom": self.prenom,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        if include_sensitive:
            data["password_hash"] = self.password_hash
        return data


# Constantes pour les rôles
ROLE_ADMIN = "ADMIN"
ROLE_SACV = "SACV"
ROLE_DCFF = "DCFF"
ROLE_DCPRE = "DCPRE"
ROLE_DTR = "DTR"
ROLE_ADHERENT = "ADHERENT"

ROLES_VALIDES = [
    ROLE_ADMIN,
    ROLE_SACV,
    ROLE_DCFF,
    ROLE_DCPRE,
    ROLE_DTR,
    ROLE_ADHERENT
]
