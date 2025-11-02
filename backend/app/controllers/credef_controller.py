from flask import Blueprint, request, jsonify
from app.extensions import db
from app.domain.repositories.credef_dossier_repo import CredefDossierRepo
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
    svc = CredefService(db.session)
    d = svc.transition(dossier_id, to, role)
    return jsonify({"id": d.id, "ref": d.ref, "statut": d.statut})
