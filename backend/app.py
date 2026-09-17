from pathlib import Path
from flask import Flask, jsonify, redirect, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from backend.config import Config
from backend.extensions import close_db, init_db


def create_app(test_config=None):
    app = Flask(__name__, static_folder=None)
    app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    if app.config["ENVIRONMENT"] == "production" and app.config["SECRET_KEY"] == "development-only-change-me":
        raise RuntimeError("SECRET_KEY must be configured in production.")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    app.teardown_appcontext(close_db)
    with app.app_context(): init_db()
    from backend.routes import auth_routes, business_routes, lead_routes, scoring_routes, outreach_routes, analytics_routes, export_routes, followup_routes, license_routes
    for route in (auth_routes.bp, business_routes.bp, lead_routes.bp, scoring_routes.bp, outreach_routes.bp, analytics_routes.bp, export_routes.bp, followup_routes.bp, license_routes.bp): app.register_blueprint(route)
    root = Path(app.root_path).parent
    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response
    @app.get("/api/health")
    def health():
        from backend.extensions import execute
        try:
            execute("SELECT 1").fetchone()
            return jsonify({"status": "ok", "database": "connected"})
        except Exception:
            return jsonify({"status": "degraded", "database": "unavailable"}), 503
    @app.get("/")
    def dashboard(): return redirect("/frontend/index.html")
    @app.get("/frontend/<path:path>")
    def frontend(path): return send_from_directory(root / "frontend", path)
    return app


app = create_app()


if __name__ == "__main__":
    import os
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
