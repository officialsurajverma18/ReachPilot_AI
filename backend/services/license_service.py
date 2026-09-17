"""License access for the existing Supabase `licenses` and `usage` tables.

All credentials stay in Render/Supabase environment variables.  The browser only
ever calls the Flask API; it never receives DATABASE_URL or a Supabase secret.
"""
from datetime import datetime, timezone
from backend.extensions import execute


def normalize_key(value):
    return (value or "").strip().replace(" ", "").upper()


def _row_to_license(row):
    return dict(row) if row else None


def find_key_by_email(email):
    row = execute('SELECT "key", email, plan, status, lead_cap, active, expires_at FROM licenses WHERE lower(email)=lower(?) ORDER BY created_at DESC LIMIT 1', (email.strip(),)).fetchone()
    license_data = _row_to_license(row)
    if not license_data:
        return None
    if not _is_active(license_data):
        return None
    return license_data


def activate_key(key):
    row = execute('SELECT "key", email, plan, status, lead_cap, active, expires_at FROM licenses WHERE "key"=? LIMIT 1', (normalize_key(key),)).fetchone()
    license_data = _row_to_license(row)
    if not license_data or not _is_active(license_data):
        return None
    return license_data


def _is_active(license_data):
    if license_data.get("active") is False:
        return False
    if (license_data.get("status") or "active").lower() not in {"active", "trial"}:
        return False
    expiry = license_data.get("expires_at")
    if expiry:
        if isinstance(expiry, str):
            try:
                expiry = datetime.fromisoformat(expiry.replace("Z", "+00:00"))
            except ValueError:
                return False
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
        if expiry < datetime.now(timezone.utc):
            return False
    return True


def usage_for_key(key, month_bucket):
    row = execute('SELECT leads_used FROM usage WHERE "key"=? AND month_bucket=?', (normalize_key(key), month_bucket)).fetchone()
    return int(row["leads_used"] if row else 0)


def record_usage(key, amount, month_bucket):
    """Track discovery usage in the existing per-license, per-month table."""
    if amount <= 0:
        return usage_for_key(key, month_bucket)
    execute('INSERT INTO usage ("key", month_bucket, leads_used) VALUES (?,?,?) ON CONFLICT ("key", month_bucket) DO UPDATE SET leads_used=usage.leads_used + excluded.leads_used', (normalize_key(key), month_bucket, amount))
    return usage_for_key(key, month_bucket)
