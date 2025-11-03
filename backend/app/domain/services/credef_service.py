from app.domain.repositories.credef_dossier_repo import CredefDossierRepo
from app.domain.repositories.workflow_log_repo import WorkflowLogRepo
from app.extensions import db

TRANSITIONS = {
    "BROUILLON": ["DÉPOSÉ"],
    "DÉPOSÉ": ["EN_CONTROLE_SACV", "REJET_ADMIN"],
    "EN_CONTROLE_SACV": ["TRANSMIS_COURRIER", "REJET_ADMIN"],
    "TRANSMIS_COURRIER": ["EN_ETUDE_PRET"],
    "EN_ETUDE_PRET": ["SOUMIS_COMITE"],
    "SOUMIS_COMITE": ["VALIDÉ_COMITE", "CLOS"],
    "VALIDÉ_COMITE": ["ETATS_EDITES"],
    "ETATS_EDITES": ["EN_SIGNATURE_DCFF_DCPRE"],
    "EN_SIGNATURE_DCFF_DCPRE": ["TRANSMIS_DTR"],
    "TRANSMIS_DTR": ["DECAISSE_ECOBANK"],
    "DECAISSE_ECOBANK": ["CLOS"],
    "REJET_ADMIN": ["BROUILLON", "DÉPOSÉ"]
}


class CredefService:
    def __init__(self, session):
        self.repo = CredefDossierRepo(session)
        self.workflow_log_repo = WorkflowLogRepo(session)

    def transition(self, dossier_id: int, to: str, role: str, note: str = "", acteur_id: int = None):
        d = self.repo.get(dossier_id)
        if not d:
            raise ValueError("Dossier introuvable")
        allowed = TRANSITIONS.get(d.statut, [])
        if to not in allowed:
            raise ValueError(f"Transition {d.statut} -> {to} non autorisée")

        # Capturer le statut actuel avant transition
        statut_from = d.statut

        # Effectuer la transition
        d.statut = to
        db.session.add(d)
        db.session.commit()

        # Logger la transition dans workflow_log
        self.workflow_log_repo.create(
            dossier_id=dossier_id,
            statut_from=statut_from,
            statut_to=to,
            acteur_id=acteur_id,
            role=role,
            commentaire=note if note else None
        )

        return d
