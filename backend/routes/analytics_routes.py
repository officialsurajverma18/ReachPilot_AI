from flask import Blueprint, jsonify
from backend.services.analytics_service import dashboard_metrics

bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")
@bp.get("/dashboard")
def dashboard(): return jsonify(dashboard_metrics())
