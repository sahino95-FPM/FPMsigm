import os
from werkzeug.utils import secure_filename
from app.domain.repositories.piece_jointe_repo import PieceJointeRepo
from app.domain.repositories.credef_dossier_repo import CredefDossierRepo


# Types de pièces acceptés avec leurs extensions autorisées
TYPES_PIECES_VALIDES = {
    "CNI": {"extensions": [".pdf", ".jpg", ".jpeg", ".png"], "obligatoire": True},
    "BULLETIN_PAIE": {"extensions": [".pdf"], "obligatoire": True},
    "ATTESTATION_TRAVAIL": {"extensions": [".pdf"], "obligatoire": True},
    "RIB": {"extensions": [".pdf", ".jpg", ".jpeg", ".png"], "obligatoire": True},
    "JUSTIFICATIF_DOMICILE": {"extensions": [".pdf"], "obligatoire": False},
    "PHOTO": {"extensions": [".jpg", ".jpeg", ".png"], "obligatoire": False},
    "AUTRE": {"extensions": [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"], "obligatoire": False}
}

# Taille maximale: 5 MB
MAX_FILE_SIZE = 5 * 1024 * 1024


class PieceJointeService:
    def __init__(self, session, upload_dir):
        self.repo = PieceJointeRepo(session)
        self.dossier_repo = CredefDossierRepo(session)
        self.upload_dir = upload_dir

    def upload_piece(self, dossier_id, type_piece, file, uploaded_by=None, commentaire=None):
        """
        Upload une pièce jointe pour un dossier

        Args:
            dossier_id: ID du dossier
            type_piece: Type de pièce (CNI, BULLETIN_PAIE, etc.)
            file: FileStorage object from Flask
            uploaded_by: ID de l'utilisateur qui upload
            commentaire: Commentaire optionnel

        Returns:
            PieceJointe object

        Raises:
            ValueError: Si validation échoue
        """
        # Vérifier que le dossier existe
        dossier = self.dossier_repo.get(dossier_id)
        if not dossier:
            raise ValueError("Dossier introuvable")

        # Vérifier le type de pièce
        if type_piece not in TYPES_PIECES_VALIDES:
            raise ValueError(f"Type de pièce invalide. Types acceptés: {', '.join(TYPES_PIECES_VALIDES.keys())}")

        # Vérifier le nom du fichier
        if not file or not file.filename:
            raise ValueError("Fichier manquant")

        # Vérifier l'extension
        filename = secure_filename(file.filename)
        _, ext = os.path.splitext(filename)
        ext_lower = ext.lower()

        allowed_extensions = TYPES_PIECES_VALIDES[type_piece]["extensions"]
        if ext_lower not in allowed_extensions:
            raise ValueError(f"Extension non autorisée pour {type_piece}. Extensions acceptées: {', '.join(allowed_extensions)}")

        # Vérifier la taille du fichier
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"Fichier trop volumineux. Taille maximale: {MAX_FILE_SIZE / (1024 * 1024):.1f} MB")

        if file_size == 0:
            raise ValueError("Fichier vide")

        # Créer le répertoire de stockage si nécessaire
        dossier_dir = os.path.join(self.upload_dir, f"dossier_{dossier_id}")
        os.makedirs(dossier_dir, exist_ok=True)

        # Générer un nom unique pour éviter les conflits
        base_name, ext = os.path.splitext(filename)
        unique_filename = f"{type_piece}_{base_name}{ext}"
        counter = 1
        while os.path.exists(os.path.join(dossier_dir, unique_filename)):
            unique_filename = f"{type_piece}_{base_name}_{counter}{ext}"
            counter += 1

        # Sauvegarder le fichier
        file_path = os.path.join(dossier_dir, unique_filename)
        file.save(file_path)

        # Créer l'enregistrement en base
        piece = self.repo.create(
            dossier_id=dossier_id,
            type_piece=type_piece,
            nom_fichier=filename,
            chemin_stockage=file_path,
            taille_octets=file_size,
            mime_type=file.content_type,
            est_obligatoire=TYPES_PIECES_VALIDES[type_piece]["obligatoire"],
            est_valide=True,  # Par défaut valide, peut être changé manuellement
            uploaded_by=uploaded_by,
            commentaire=commentaire
        )

        return piece

    def get_pieces_dossier(self, dossier_id):
        """Récupère toutes les pièces d'un dossier"""
        return self.repo.get_by_dossier(dossier_id)

    def delete_piece(self, piece_id):
        """
        Supprime une pièce jointe (fichier + BDD)

        Returns:
            True si suppression réussie, False sinon
        """
        piece = self.repo.get(piece_id)
        if not piece:
            return False

        # Supprimer le fichier physique
        if os.path.exists(piece.chemin_stockage):
            try:
                os.remove(piece.chemin_stockage)
            except Exception as e:
                # Log l'erreur mais continue la suppression en BDD
                print(f"Erreur suppression fichier {piece.chemin_stockage}: {e}")

        # Supprimer l'enregistrement en BDD
        return self.repo.delete(piece_id)

    def valider_completude_dossier(self, dossier_id):
        """
        Vérifie si toutes les pièces obligatoires sont présentes

        Returns:
            dict avec "complet" (bool) et "pieces_manquantes" (list)
        """
        types_obligatoires = [
            type_piece for type_piece, config in TYPES_PIECES_VALIDES.items()
            if config["obligatoire"]
        ]

        pieces_manquantes = self.repo.get_pieces_obligatoires_manquantes(
            dossier_id, types_obligatoires
        )

        return {
            "complet": len(pieces_manquantes) == 0,
            "pieces_manquantes": pieces_manquantes,
            "types_obligatoires": types_obligatoires
        }
