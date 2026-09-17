from backend.extensions import execute


def dashboard_metrics():
    def scalar(sql, params=()):
        row = execute(sql, params).fetchone()
        return row[0] if row else 0
    return {"total_leads": scalar("SELECT COUNT(*) FROM leads"), "high_score_leads": scalar("SELECT COUNT(*) FROM leads WHERE score >= 70"),
            "qualified_leads": scalar("SELECT COUNT(*) FROM leads WHERE score >= 40"), "outreach_activity": scalar("SELECT COUNT(*) FROM communications"),
            "pending_followups": scalar("SELECT COUNT(*) FROM followups WHERE status='pending'"),
            "status_distribution": [{"status": row[0], "count": row[1]} for row in execute("SELECT status, COUNT(*) FROM leads GROUP BY status").fetchall()]}
