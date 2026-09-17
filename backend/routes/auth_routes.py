from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from backend.extensions import execute, insert_id
from backend.utils.validators import required, valid_email

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    try:
        required(data, "name", "email", "password")
        if not valid_email(data["email"]): raise ValueError("Enter a valid email address.")
        user_id = insert_id("INSERT INTO users (name,email,password_hash) VALUES (?,?,?)", (data["name"].strip(), data["email"].strip().lower(), generate_password_hash(data["password"])))
        session["user_id"] = user_id
        return jsonify({"id": user_id, "name": data["name"], "email": data["email"]}), 201
    except ValueError as error: return jsonify({"error": str(error)}), 400
    except Exception: return jsonify({"error": "An account with that email already exists."}), 409

@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    row = execute("SELECT * FROM users WHERE email=?", ((data.get("email") or "").strip().lower(),)).fetchone()
    if not row or not check_password_hash(row["password_hash"], data.get("password") or ""):
        return jsonify({"error": "Invalid email or password."}), 401
    session["user_id"] = row["id"]
    return jsonify({"id": row["id"], "name": row["name"], "email": row["email"]})

@bp.post("/logout")
def logout(): session.clear(); return "", 204
