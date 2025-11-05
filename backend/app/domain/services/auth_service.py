from flask_jwt_extended import create_access_token, create_refresh_token
from app.domain.repositories.user_repo import UserRepo
from app.domain.models.user import ROLES_VALIDES


class AuthService:
    def __init__(self, session):
        self.repo = UserRepo(session)

    def register(self, email, password, nom, prenom, role):
        """
        Enregistre un nouvel utilisateur

        Args:
            email: Email de l'utilisateur (unique)
            password: Mot de passe en clair (sera hashé)
            nom: Nom de l'utilisateur
            prenom: Prénom de l'utilisateur
            role: Rôle de l'utilisateur (ADMIN, SACV, etc.)

        Returns:
            User object

        Raises:
            ValueError: Si email déjà utilisé ou rôle invalide
        """
        # Vérifier si l'email existe déjà
        existing_user = self.repo.get_by_email(email)
        if existing_user:
            raise ValueError("Un utilisateur avec cet email existe déjà")

        # Vérifier que le rôle est valide
        if role not in ROLES_VALIDES:
            raise ValueError(f"Rôle invalide. Rôles valides: {', '.join(ROLES_VALIDES)}")

        # Créer l'utilisateur
        user = self.repo.model(
            email=email,
            nom=nom,
            prenom=prenom,
            role=role,
            is_active=True
        )

        # Hash du mot de passe
        user.set_password(password)

        # Sauvegarder
        self.repo.session.add(user)
        self.repo.session.commit()
        self.repo.session.refresh(user)

        return user

    def login(self, email, password):
        """
        Authentifie un utilisateur

        Args:
            email: Email de l'utilisateur
            password: Mot de passe en clair

        Returns:
            dict avec access_token, refresh_token et user

        Raises:
            ValueError: Si identifiants invalides ou compte inactif
        """
        # Récupérer l'utilisateur
        user = self.repo.get_by_email(email)
        if not user:
            raise ValueError("Email ou mot de passe incorrect")

        # Vérifier le mot de passe
        if not user.check_password(password):
            raise ValueError("Email ou mot de passe incorrect")

        # Vérifier que le compte est actif
        if not user.is_active:
            raise ValueError("Ce compte est désactivé")

        # Créer les tokens JWT
        # Identity doit être une string (user_id), les claims additionnels contiennent email et role
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"email": user.email, "role": user.role}
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={"email": user.email, "role": user.role}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }

    def get_user_by_id(self, user_id):
        """Récupère un utilisateur par son ID"""
        return self.repo.get(user_id)

    def get_user_by_email(self, email):
        """Récupère un utilisateur par son email"""
        return self.repo.get_by_email(email)
