import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def required(payload, *fields):
    missing = [field for field in fields if not str(payload.get(field, "")).strip()]
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")


def valid_email(value):
    return bool(EMAIL_RE.match((value or "").strip()))
