from flask import Blueprint, request, jsonify
from app.extensions import db
from app.domain.repositories.credef_dossier_repo import CredefDossierRepo
from app.domain.repositories.workflow_log_repo import WorkflowLogRepo
from app.domain.services.credef_service import CredefService


bp = Blueprint("credef", __name__, url_prefix="/api/credef")


@bp.get("/dossiers")
def list_dossiers():
    statut = request.args.get("statut")
    mois = request.args.get("mois")
    repo = CredefDossierRepo(db.session)
    items = repo.list(statut, mois)
    return jsonify([{"id": x.id, "ref": x.ref, "statut": x.statut} for x in items])


@bp.post("/dossiers")
def create_dossier():
    data = request.get_json() or {}
    repo = CredefDossierRepo(db.session)
    obj = repo.create(**data)
    return jsonify({"id": obj.id, "ref": obj.ref, "statut": obj.statut}), 201


@bp.post("/dossiers/<int:dossier_id>/transition")
def transition(dossier_id):
    payload = request.get_json() or {}
    to = payload.get("to")
    role = payload.get("role", "SYSTEM")
    note = payload.get("note", "")
    acteur_id = payload.get("acteur_id")
    svc = CredefService(db.session)
    d = svc.transition(dossier_id, to, role, note=note, acteur_id=acteur_id)
    return jsonify({"id": d.id, "ref": d.ref, "statut": d.statut})


@bp.get("/dossiers/<int:dossier_id>/workflow")
def get_workflow_history(dossier_id):
    """Récupère l'historique complet des transitions d'un dossier"""
    # Vérifier que le dossier existe
    dossier_repo = CredefDossierRepo(db.session)
    dossier = dossier_repo.get(dossier_id)
    if not dossier:
        return jsonify({"error": "Dossier introuvable"}), 404

    # Récupérer l'historique des transitions
    workflow_repo = WorkflowLogRepo(db.session)
    logs = workflow_repo.get_by_dossier(dossier_id)

    return jsonify({
        "dossier_id": dossier_id,
        "dossier_ref": dossier.ref,
        "statut_actuel": dossier.statut,
        "historique": [log.to_dict() for log in logs]
    })
