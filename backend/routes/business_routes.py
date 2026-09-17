from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from backend.services.maps_service import search_businesses
from backend.services.lead_service import create_from_business
from backend.services.contact_enrichment_service import find_public_email
from backend.extensions import execute
from backend.utils.validators import required
from backend.middleware.license import require_active_license
from backend.services.license_service import record_usage, usage_for_key

bp = Blueprint("businesses", __name__, url_prefix="/api/businesses")

@bp.post("/search")
@require_active_license
def search():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "keyword", "location")
        requested_limit = min(max(int(data.get("limit", 20)), 1), 20)
        license_data = getattr(request, "license_data", None)
        month_bucket = datetime.now(timezone.utc).strftime("%Y-%m")
        if license_data and license_data.get("lead_cap") is not None:
            used = usage_for_key(license_data["key"], month_bucket)
            remaining = max(0, int(license_data["lead_cap"]) - used)
            if remaining == 0:
                return jsonify({"error": "Your monthly lead limit has been reached."}), 429
            requested_limit = min(requested_limit, remaining)
        results = search_businesses(data["keyword"], data["location"], data.get("category", ""), requested_limit)
        leads = [create_from_business(item) for item in results]
        usage = record_usage(license_data["key"], len(results), month_bucket) if license_data else None
        return jsonify({"results": results, "leads": leads, "count": len(results), "usage": usage})
    except ValueError as error: return jsonify({"error": str(error)}), 400
    except RuntimeError as error: return jsonify({"error": str(error)}), 503
    except Exception: return jsonify({"error": "Business search failed. Check the server configuration."}), 502

@bp.post("/enrich-emails")
def enrich_emails():
    """Find publicly listed emails for saved leads that have a website."""
    rows = execute("SELECT l.id, b.website FROM leads l JOIN businesses b ON b.id=l.business_id WHERE (b.email IS NULL OR b.email='') AND b.website IS NOT NULL AND b.website != ''").fetchall()
    updated, skipped = [], 0
    for row in rows:
        emails = find_public_email(row["website"])
        if emails:
            execute("UPDATE businesses SET email=? WHERE id=(SELECT business_id FROM leads WHERE id=?)", (emails[0], row["id"]))
            updated.append({"lead_id": row["id"], "email": emails[0]})
        else:
            skipped += 1
    return jsonify({"checked": len(rows), "found": len(updated), "not_found": skipped, "results": updated})
