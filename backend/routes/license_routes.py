from flask import Blueprint, current_app, jsonify, request, session
from backend.services.license_service import activate_key, find_key_by_email
from backend.utils.validators import required, valid_email

bp = Blueprint("licenses", __name__, url_prefix="/api/licenses")


def _configured():
    return bool(current_app.config.get("DATABASE_URL"))


@bp.post("/find-key")
def find_key():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "email")
        if not valid_email(data["email"]):
            raise ValueError("Enter a valid purchase email.")
        if not _configured():
            current_app.logger.error("License lookup requested without DATABASE_URL configured")
            return jsonify({"error": "License service is temporarily unavailable. Please try again later."}), 503
        result = find_key_by_email(data["email"])
        if not result:
            return jsonify({"error": "No active key found for this email. Please register or contact support."}), 404
        return jsonify({"key": result["key"], "email": result["email"], "plan": result.get("plan"), "lead_cap": result.get("lead_cap")})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        current_app.logger.exception("License lookup failed")
        return jsonify({"error": "Could not check the license database."}), 503


@bp.post("/activate")
def activate():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "key")
        if not _configured():
            current_app.logger.error("License activation requested without DATABASE_URL configured")
            return jsonify({"error": "License service is temporarily unavailable. Please try again later."}), 503
        result = activate_key(data["key"])
        if not result:
            return jsonify({"error": "Invalid, inactive, or expired activation key."}), 401
        session["license_key"] = result["key"]
        session["license_email"] = result["email"]
        return jsonify({"valid": True, "email": result["email"], "plan": result.get("plan"), "lead_cap": result.get("lead_cap")})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        current_app.logger.exception("License activation failed")
        return jsonify({"error": "Could not validate the activation key."}), 503
