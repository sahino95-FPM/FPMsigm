from .base import Repository
from app.domain.models.workflow_log import WorkflowLog


class WorkflowLogRepo(Repository):
    model = WorkflowLog

    def get_by_dossier(self, dossier_id, limit=None):
        """Récupère l'historique des transitions pour un dossier, triées par date décroissante"""
        query = self.session.query(self.model).filter_by(dossier_id=dossier_id).order_by(self.model.created_at.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_all_logs(self, limit=None):
        """Récupère tous les logs, triés par date décroissante"""
        query = self.session.query(self.model).order_by(self.model.created_at.desc())

        if limit:
            query = query.limit(limit)

        return query.all()
