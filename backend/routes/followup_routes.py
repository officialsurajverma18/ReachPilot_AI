from flask import Blueprint, jsonify, request
from backend.extensions import execute, insert_id
from backend.utils.validators import required

bp = Blueprint("followups", __name__, url_prefix="/api/followups")
@bp.get("")
def list_all(): return jsonify([dict(row) for row in execute("SELECT f.*, b.name FROM followups f JOIN leads l ON l.id=f.lead_id JOIN businesses b ON b.id=l.business_id ORDER BY f.due_at").fetchall()])
@bp.post("")
def create():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "lead_id", "due_at")
        followup_id = insert_id("INSERT INTO followups (lead_id,due_at,note) VALUES (?,?,?)", (data["lead_id"], data["due_at"], data.get("note", "")))
        return jsonify(dict(execute("SELECT * FROM followups WHERE id=?", (followup_id,)).fetchone())), 201
    except ValueError as error: return jsonify({"error": str(error)}), 400
@bp.put("/<int:followup_id>")
def update(followup_id):
    data = request.get_json(silent=True) or {}
    if data.get("status") not in {"pending", "completed"}: return jsonify({"error": "Status must be pending or completed."}), 400
    execute("UPDATE followups SET status=? WHERE id=?", (data["status"], followup_id))
    return jsonify(dict(execute("SELECT * FROM followups WHERE id=?", (followup_id,)).fetchone()))
