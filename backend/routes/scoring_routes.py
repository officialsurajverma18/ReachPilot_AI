from flask import Blueprint, jsonify
from backend.services.lead_service import get_lead, rescore

bp = Blueprint("scoring", __name__, url_prefix="/api/leads")
@bp.post("/<int:lead_id>/score")
def score(lead_id):
    lead = rescore(lead_id)
    return (jsonify(lead), 200) if lead else (jsonify({"error": "Lead not found."}), 404)
@bp.get("/<int:lead_id>/score")
def score_detail(lead_id):
    lead = get_lead(lead_id)
    return (jsonify({"score": lead["score"], "priority": lead["priority"], "factors": lead["score_factors"]}), 200) if lead else (jsonify({"error": "Lead not found."}), 404)
