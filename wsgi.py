"""Production WSGI entry point for Gunicorn on Render."""
from backend.app import create_app

app = create_app()
