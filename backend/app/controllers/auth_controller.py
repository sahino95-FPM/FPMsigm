from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.domain.services.auth_service import AuthService
from app.domain.models.user import ROLES_VALIDES


bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
    """Créer un nouveau compte utilisateur"""
    try:
        data = request.get_json() or {}

        # Validation des champs requis
        required_fields = ["email", "password", "nom", "prenom", "role"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Le champ '{field}' est obligatoire"}), 400

        # Validation du mot de passe
        password = data.get("password", "")
        if len(password) < 6:
            return jsonify({"error": "Le mot de passe doit contenir au moins 6 caractères"}), 400

        # Créer l'utilisateur
        svc = AuthService(db.session)
        user = svc.register(
            email=data["email"],
            password=password,
            nom=data["nom"],
            prenom=data["prenom"],
            role=data["role"]
        )

        return jsonify({
            "message": "Utilisateur créé avec succès",
            "user": user.to_dict()
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création: {str(e)}"}), 500


@bp.post("/login")
def login():
    """Authentifier un utilisateur et obtenir un token JWT"""
    try:
        data = request.get_json() or {}

        # Validation des champs requis
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email et mot de passe requis"}), 400

        # Authentifier
        svc = AuthService(db.session)
        result = svc.login(email, password)

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'authentification: {str(e)}"}), 500


@bp.get("/me")
@jwt_required()
def get_current_user():
    """Récupère les informations de l'utilisateur connecté"""
    try:
        # Récupérer l'identité depuis le token JWT
        identity = get_jwt_identity()
        user_id = identity.get("user_id")

        # Récupérer l'utilisateur
        svc = AuthService(db.session)
        user = svc.get_user_by_id(user_id)

        if not user:
            return jsonify({"error": "Utilisateur introuvable"}), 404

        return jsonify(user.to_dict()), 200

    except Exception as e:
        return jsonify({"error": f"Erreur: {str(e)}"}), 500


@bp.get("/roles")
def get_roles():
    """Liste tous les rôles disponibles"""
    return jsonify({
        "roles": ROLES_VALIDES
    }), 200
