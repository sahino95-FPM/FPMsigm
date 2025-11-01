from .base import Repository
from app.domain.models.credef_dossier import CredefDossier


class CredefDossierRepo(Repository):
    model = CredefDossier

    def list(self, statut=None, mois=None):
        q = self.session.query(self.model)
        if statut:
            q = q.filter(self.model.statut == statut)
        if mois:
            q = q.filter(self.model.mois_traitement == mois)
        return q.order_by(self.model.id.desc()).all()
