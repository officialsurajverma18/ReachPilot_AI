from flask import Blueprint, jsonify, request
from backend.services.lead_service import create_from_business, get_lead, list_leads, update_lead
from backend.utils.validators import required

bp = Blueprint("leads", __name__, url_prefix="/api/leads")

@bp.get("")
def list_all(): return jsonify(list_leads(request.args.get("status"), request.args.get("min_score", type=int)))

@bp.post("")
def create():
    data = request.get_json(silent=True) or {}
    try: required(data, "name"); return jsonify(create_from_business(data)), 201
    except ValueError as error: return jsonify({"error": str(error)}), 400

@bp.get("/<int:lead_id>")
def detail(lead_id):
    lead = get_lead(lead_id)
    return (jsonify(lead), 200) if lead else (jsonify({"error": "Lead not found."}), 404)

@bp.put("/<int:lead_id>")
def update(lead_id):
    lead = update_lead(lead_id, request.get_json(silent=True) or {})
    return (jsonify(lead), 200) if lead else (jsonify({"error": "Lead not found."}), 404)

@bp.delete("/<int:lead_id>")
def delete(lead_id):
    from backend.extensions import execute
    execute("DELETE FROM leads WHERE id=?", (lead_id,)); return "", 204
