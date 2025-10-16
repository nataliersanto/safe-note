from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.encryption import encrypt_bytes, decrypt_bytes
from app.models import upload_file_bytes
from passlib.hash import bcrypt
import datetime
import os

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
    hashed = bcrypt.hash(password)
    USERS[username] = hashed
    NOTES[username] = {}
    return jsonify({"msg":"registered"}), 200

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    stored_hash = USERS.get(username)
    if not stored_hash or not bcrypt.verify(password, stored_hash):
        return jsonify({"msg": "bad credentials"}), 401
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
    encrypted = encrypt_bytes(content)
    save_note(username, title, encrypted)
    return jsonify({"msg":"saved"}), 200

@bp.route("/notes/<title>", methods=["GET"])
@jwt_required()
def get_note_route(title):
    username = get_jwt_identity()
    enc = get_note(username, title)
    if not enc:
        return jsonify({"msg":"not found"}), 404
    dec = decrypt_text(enc)
    return jsonify({"title": title, "content": dec}), 200

@bp.route("/notes/<title>/upload", methods=["POST"])
@jwt_required()
def upload_file(title):
    username = get_jwt_identity()
    file = request.files.get("file")
    if not file:
        return jsonify({"msg": "No file uploaded"}), 400

    # Read raw file bytes
    file_bytes = file.read()  # bytes

    # Encrypt bytes
    encrypted_bytes = encrypt_bytes(file_bytes)

    # Upload to S3
    bucket = os.getenv("S3_BUCKET")
    key = f"{username}/{title}/{file.filename}"
    upload_file_bytes(bucket, key, encrypted_bytes)

    return jsonify({"msg": "File uploaded successfully"}), 200
