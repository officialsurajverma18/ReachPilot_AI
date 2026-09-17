from functools import wraps
from flask import current_app, jsonify, request, session
from backend.services.license_service import activate_key


def current_license():
    key = session.get("license_key") or request.headers.get("X-License-Key", "")
    return activate_key(key) if key else None


def require_active_license(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_app.config.get("REQUIRE_LICENSE"):
            return view(*args, **kwargs)
        license_data = current_license()
        if not license_data:
            return jsonify({"error": "An active subscription is required to generate leads."}), 403
        request.license_data = license_data
        return view(*args, **kwargs)
    return wrapped
