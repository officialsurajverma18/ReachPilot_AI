from flask import Blueprint, Response
from backend.services.lead_service import list_leads
from backend.utils.csv_export import leads_csv

bp = Blueprint("export", __name__, url_prefix="/api/export")
@bp.get("/leads/csv")
def export_leads():
    return Response(leads_csv(list_leads()), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=reachpilot-leads.csv"})
