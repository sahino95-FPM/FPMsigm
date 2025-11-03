from .base import Repository
from app.domain.models.piece_jointe import PieceJointe


class PieceJointeRepo(Repository):
    model = PieceJointe

    def get_by_dossier(self, dossier_id):
        """Récupère toutes les pièces jointes d'un dossier"""
        return self.session.query(self.model).filter_by(dossier_id=dossier_id).order_by(self.model.created_at.desc()).all()

    def get_by_type(self, dossier_id, type_piece):
        """Récupère les pièces d'un type spécifique pour un dossier"""
        return self.session.query(self.model).filter_by(dossier_id=dossier_id, type_piece=type_piece).all()

    def delete(self, piece_id):
        """Supprime une pièce jointe"""
        piece = self.get(piece_id)
        if piece:
            self.session.delete(piece)
            self.session.commit()
            return True
        return False

    def get_pieces_obligatoires_manquantes(self, dossier_id, types_obligatoires):
        """
        Retourne la liste des types de pièces obligatoires manquantes pour un dossier

        Args:
            dossier_id: ID du dossier
            types_obligatoires: Liste des types de pièces obligatoires (ex: ["CNI", "BULLETIN_PAIE"])

        Returns:
            Liste des types de pièces manquantes
        """
        pieces_presentes = self.session.query(self.model.type_piece).filter_by(
            dossier_id=dossier_id
        ).distinct().all()

        types_presentes = {p[0] for p in pieces_presentes}
        types_obligatoires_set = set(types_obligatoires)

        return list(types_obligatoires_set - types_presentes)
