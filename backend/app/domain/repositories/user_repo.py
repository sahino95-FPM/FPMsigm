from .base import Repository
from app.domain.models.user import User


class UserRepo(Repository):
    model = User

    def get_by_email(self, email):
        """Récupère un utilisateur par son email"""
        return self.session.query(self.model).filter_by(email=email).first()

    def get_active_users(self):
        """Récupère tous les utilisateurs actifs"""
        return self.session.query(self.model).filter_by(is_active=True).all()

    def get_by_role(self, role):
        """Récupère tous les utilisateurs d'un rôle donné"""
        return self.session.query(self.model).filter_by(role=role).all()

    def deactivate(self, user_id):
        """Désactive un utilisateur"""
        user = self.get(user_id)
        if user:
            user.is_active = False
            self.session.commit()
            return True
        return False

    def activate(self, user_id):
        """Active un utilisateur"""
        user = self.get(user_id)
        if user:
            user.is_active = True
            self.session.commit()
            return True
        return False
