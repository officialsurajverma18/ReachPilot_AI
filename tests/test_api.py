import tempfile
from pathlib import Path
from backend.app import create_app


def app_client():
    path = Path(tempfile.gettempdir()) / "reachpilot-test.sqlite3"
    if path.exists(): path.unlink()
    app = create_app({"TESTING": True, "SQLITE_PATH": str(path), "SECRET_KEY": "test"})
    return app.test_client()


def test_health_and_lead_workflow():
    client = app_client()
    assert client.get("/api/health").status_code == 200
    created = client.post("/api/leads", json={"name": "Example Studio", "location": "Kanpur", "rating": 4.3, "review_count": 80, "website": "https://example.com", "phone": "+919999999999"})
    assert created.status_code == 201
    lead = created.get_json()
    assert lead["score"] > 0 and lead["score_factors"]
    assert client.put(f"/api/leads/{lead['id']}", json={"status": "Contacted", "notes": "Call Thursday"}).get_json()["status"] == "Contacted"
    assert client.get("/api/export/leads/csv").status_code == 200


def test_auth_followup_and_outreach_draft():
    client = app_client()
    assert client.post("/api/auth/register", json={"name": "Student", "email": "student@example.com", "password": "safe-password"}).status_code == 201
    lead = client.post("/api/leads", json={"name": "Sample Agency", "phone": "+91 99999 99999"}).get_json()
    draft = client.post("/api/outreach/generate-message", json={"lead_id": lead["id"]})
    assert draft.status_code == 200 and draft.get_json()["provider"] == "template"
    followup = client.post("/api/followups", json={"lead_id": lead["id"], "due_at": "2026-10-01T10:00:00", "note": "Check in"})
    assert followup.status_code == 201
    assert client.put(f"/api/followups/{followup.get_json()['id']}", json={"status": "completed"}).get_json()["status"] == "completed"


def test_license_lookup_requires_render_database_configuration():
    client = app_client()
    response = client.post("/api/licenses/find-key", json={"email": "buyer@example.com"})
    assert response.status_code == 503
    assert response.get_json()["error"] == "License service is temporarily unavailable. Please try again later."


def test_production_license_guard_blocks_discovery_without_an_active_key():
    path = Path(tempfile.gettempdir()) / "reachpilot-license-guard.sqlite3"
    if path.exists(): path.unlink()
    app = create_app({"TESTING": True, "SQLITE_PATH": str(path), "SECRET_KEY": "test", "REQUIRE_LICENSE": True})
    response = app.test_client().post("/api/businesses/search", json={"keyword": "Agency", "location": "Kanpur"})
    assert response.status_code == 403
