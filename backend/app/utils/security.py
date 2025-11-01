from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from flask import jsonify


def jwt_required_role(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(optional=True)  # pour POC, tolérant
            claims = get_jwt() or {}
            user_roles = claims.get("roles", ["ADMIN"])
            if not set(user_roles).intersection(set(roles)):
                return jsonify({"error": "role_not_allowed"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
