from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.domain.repositories.credef_dossier_repo import CredefDossierRepo
from app.domain.repositories.workflow_log_repo import WorkflowLogRepo
from app.domain.services.credef_service import CredefService
from app.domain.services.piece_jointe_service import PieceJointeService


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


@bp.post("/dossiers/<int:dossier_id>/pieces")
def upload_piece(dossier_id):
    """Upload une pièce jointe pour un dossier"""
    try:
        # Vérifier qu'un fichier est présent
        if 'file' not in request.files:
            return jsonify({"error": "Aucun fichier fourni"}), 400

        file = request.files['file']
        type_piece = request.form.get('type_piece')
        uploaded_by = request.form.get('uploaded_by')
        commentaire = request.form.get('commentaire')

        if not type_piece:
            return jsonify({"error": "Le type de pièce est obligatoire"}), 400

        # Upload du fichier
        upload_dir = current_app.config.get('UPLOAD_DIR', '/tmp/uploads')
        svc = PieceJointeService(db.session, upload_dir)
        piece = svc.upload_piece(
            dossier_id=dossier_id,
            type_piece=type_piece,
            file=file,
            uploaded_by=int(uploaded_by) if uploaded_by else None,
            commentaire=commentaire
        )

        return jsonify(piece.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'upload: {str(e)}"}), 500


@bp.get("/dossiers/<int:dossier_id>/pieces")
def list_pieces(dossier_id):
    """Liste toutes les pièces jointes d'un dossier"""
    # Vérifier que le dossier existe
    dossier_repo = CredefDossierRepo(db.session)
    dossier = dossier_repo.get(dossier_id)
    if not dossier:
        return jsonify({"error": "Dossier introuvable"}), 404

    # Récupérer les pièces
    upload_dir = current_app.config.get('UPLOAD_DIR', '/tmp/uploads')
    svc = PieceJointeService(db.session, upload_dir)
    pieces = svc.get_pieces_dossier(dossier_id)

    return jsonify({
        "dossier_id": dossier_id,
        "dossier_ref": dossier.ref,
        "pieces": [piece.to_dict() for piece in pieces]
    })


@bp.get("/dossiers/<int:dossier_id>/pieces/validation")
def validate_completude(dossier_id):
    """Vérifie si toutes les pièces obligatoires sont présentes"""
    # Vérifier que le dossier existe
    dossier_repo = CredefDossierRepo(db.session)
    dossier = dossier_repo.get(dossier_id)
    if not dossier:
        return jsonify({"error": "Dossier introuvable"}), 404

    # Valider la complétude
    upload_dir = current_app.config.get('UPLOAD_DIR', '/tmp/uploads')
    svc = PieceJointeService(db.session, upload_dir)
    validation = svc.valider_completude_dossier(dossier_id)

    return jsonify({
        "dossier_id": dossier_id,
        "dossier_ref": dossier.ref,
        **validation
    })


@bp.delete("/pieces/<int:piece_id>")
def delete_piece(piece_id):
    """Supprime une pièce jointe"""
    upload_dir = current_app.config.get('UPLOAD_DIR', '/tmp/uploads')
    svc = PieceJointeService(db.session, upload_dir)

    if svc.delete_piece(piece_id):
        return jsonify({"message": "Pièce supprimée avec succès"}), 200
    else:
        return jsonify({"error": "Pièce introuvable"}), 404
