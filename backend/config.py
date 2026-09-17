import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


ROOT = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development").strip().lower()
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
    SQLITE_PATH = os.getenv("SQLITE_PATH", str(ROOT / "instance" / "reachpilot.sqlite3"))
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "").strip()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "").strip()
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM = os.getenv("SMTP_FROM", "").strip()
    REQUIRE_LICENSE = os.getenv("REQUIRE_LICENSE", "false").strip().lower() in {"1", "true", "yes"}
    SESSION_COOKIE_SECURE = ENVIRONMENT == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
