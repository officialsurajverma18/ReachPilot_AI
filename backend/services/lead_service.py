import json
from backend.extensions import execute, insert_id
from backend.services.scoring_service import score_business


SELECT = """SELECT l.id, l.status, l.priority, l.score, l.score_factors, l.notes, l.created_at, l.updated_at,
b.id AS business_id, b.name, b.category, b.location, b.address, b.phone, b.email, b.website, b.maps_url, b.rating, b.review_count
FROM leads l JOIN businesses b ON b.id=l.business_id"""

def _dict(row):
    item = dict(row)
    item["score_factors"] = json.loads(item.get("score_factors") or "[]")
    return item

def list_leads(status=None, minimum_score=None):
    sql, params = SELECT, []
    clauses = []
    if status: clauses.append("l.status=?"); params.append(status)
    if minimum_score is not None: clauses.append("l.score>=?"); params.append(minimum_score)
    if clauses: sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY l.score DESC, l.updated_at DESC"
    return [_dict(row) for row in execute(sql, params).fetchall()]

def get_lead(lead_id):
    row = execute(SELECT + " WHERE l.id=?", (lead_id,)).fetchone()
    return _dict(row) if row else None

def create_from_business(data):
    score, priority, factors = score_business(data)
    existing = execute("SELECT id FROM businesses WHERE place_id=? OR (name=? AND address=?)", (data.get("place_id") or "", data["name"], data.get("address") or "")).fetchone()
    if existing:
        lead = execute("SELECT id FROM leads WHERE business_id=?", (existing[0],)).fetchone()
        return get_lead(lead[0]) if lead else None
    business_id = insert_id("INSERT INTO businesses (place_id,name,category,location,address,phone,email,website,maps_url,rating,review_count,source_query) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (data.get("place_id"), data["name"], data.get("category"), data.get("location"), data.get("address"), data.get("phone"), data.get("email"), data.get("website"), data.get("maps_url"), data.get("rating") or 0, data.get("review_count") or 0, data.get("source_query")))
    lead_id = insert_id("INSERT INTO leads (business_id,status,priority,score,score_factors) VALUES (?,?,?,?,?)", (business_id, "New", priority, score, json.dumps(factors)))
    return get_lead(lead_id)

def update_lead(lead_id, data):
    allowed = {"status", "priority", "notes"}
    changes = {key: value for key, value in data.items() if key in allowed}
    if not changes: return get_lead(lead_id)
    fields = list(changes); values = [changes[key] for key in fields]
    execute("UPDATE leads SET " + ", ".join(f"{field}=?" for field in fields) + ", updated_at=CURRENT_TIMESTAMP WHERE id=?", values + [lead_id])
    return get_lead(lead_id)

def rescore(lead_id):
    lead = get_lead(lead_id)
    if not lead: return None
    score, priority, factors = score_business(lead)
    execute("UPDATE leads SET score=?, priority=?, score_factors=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (score, priority, json.dumps(factors), lead_id))
    return get_lead(lead_id)
