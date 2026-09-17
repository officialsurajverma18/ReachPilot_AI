from flask import Blueprint, jsonify, request
from backend.extensions import execute, insert_id
from backend.services.ai_writer_service import generate_message
from backend.services.lead_service import get_lead
from backend.services.email_service import send_email
from backend.utils.validators import required

bp = Blueprint("outreach", __name__, url_prefix="/api/outreach")

@bp.post("/generate-message")
def generate():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "lead_id")
        lead = get_lead(int(data["lead_id"]))
        if not lead: return jsonify({"error": "Lead not found."}), 404
        message, provider = generate_message(lead, data.get("tone", "professional"))
        communication_id = insert_id("INSERT INTO communications (lead_id,channel,message,status) VALUES (?,?,?,?)", (lead["id"], "email", message, "draft"))
        return jsonify({"id": communication_id, "lead_id": lead["id"], "message": message, "provider": provider, "status": "draft"})
    except ValueError as error: return jsonify({"error": str(error)}), 400

@bp.get("/history/<int:lead_id>")
def history(lead_id):
    return jsonify([dict(row) for row in execute("SELECT * FROM communications WHERE lead_id=? ORDER BY created_at DESC", (lead_id,)).fetchall()])

@bp.post("/email")
def send():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "lead_id", "subject", "message")
        lead = get_lead(int(data["lead_id"]))
        if not lead: return jsonify({"error": "Lead not found."}), 404
        if not lead.get("email"): return jsonify({"error": "This lead has no public email address."}), 400
        send_email(lead["email"], data["subject"], data["message"])
        communication_id = insert_id("INSERT INTO communications (lead_id,channel,subject,message,status) VALUES (?,?,?,?,?)", (lead["id"], "email", data["subject"], data["message"], "sent"))
        return jsonify({"id": communication_id, "status": "sent"})
    except ValueError as error: return jsonify({"error": str(error)}), 400

@bp.post("/whatsapp-link")
def whatsapp_link():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "lead_id", "message")
        lead = get_lead(int(data["lead_id"]))
        if not lead or not lead.get("phone"): return jsonify({"error": "Lead has no phone number."}), 400
        import re
        from urllib.parse import quote
        number = re.sub(r"\D", "", lead["phone"])
        return jsonify({"url": f"https://wa.me/{number}?text={quote(data['message'])}", "mode": "draft"})
    except ValueError as error: return jsonify({"error": str(error)}), 400
