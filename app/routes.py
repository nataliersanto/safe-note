from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.encryption import encrypt_text, decrypt_text
import datetime

bp = Blueprint("routes", __name__)

USERS = {}     # username -> password (hashed in real app)
NOTES = {}     # username -> {title: encrypted_content}

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg":"username & password required"}), 400
    if username in USERS:
        return jsonify({"msg":"user exists"}), 400
    USERS[username] = password  # NOTE: for demo only, hash in real app!
    NOTES[username] = {}
    return jsonify({"msg":"registered"}), 200

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) != password:
        return jsonify({"msg":"bad credentials"}), 401
    token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))
    return jsonify({"access_token": token}), 200

@bp.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    username = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return jsonify({"msg":"title and content required"}), 400
    encrypted = encrypt_text(content)
    NOTES[username][title] = encrypted
    return jsonify({"msg":"saved"}), 200

@bp.route("/notes/<title>", methods=["GET"])
@jwt_required()
def get_note(title):
    username = get_jwt_identity()
    enc = NOTES.get(username, {}).get(title)
    if not enc:
        return jsonify({"msg":"not found"}), 404
    dec = decrypt_text(enc)
    return jsonify({"title": title, "content": dec}), 200