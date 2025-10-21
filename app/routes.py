from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.encryption import encrypt_bytes, decrypt_bytes
from app.models import upload_file_bytes, save_note, get_note
from passlib.hash import bcrypt
import datetime
import os
import boto3

bp = Blueprint("routes", __name__)

dynamo = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION"))
users_table = dynamo.Table(os.getenv("USERS_TABLE"))
notes_table = dynamo.Table(os.getenv("DYNAMODB_TABLE"))

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "username & password required"}), 400
    resp = users_table.get_item(Key={"username": username})
    if "Item" in resp:
        return jsonify({"msg": "user exists"}), 400
    truncated_password = password.encode("utf-8")[:72] 
    hashed = bcrypt.hash(truncated_password)
    users_table.put_item(
        Item={
            "username": username,    
            "password_hash": hashed,               
            "created_at": str(datetime.datetime.utcnow())  
        }
    )
    return jsonify({"msg": "registered"}), 200

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"msg": "username & password required"}), 400
    resp = users_table.get_item(Key={"username": username})
    user_item = resp.get("Item")
    if not user_item:
        return jsonify({"msg": "bad credentials"}), 401
    stored_hash = user_item["password_hash"]
    if not bcrypt.verify(password.encode("utf-8")[:72], stored_hash):
        return jsonify({"msg": "bad credentials"}), 401
    token = create_access_token(
        identity=username,
        expires_delta=datetime.timedelta(hours=1)
    )
    return jsonify({"access_token": token}), 200

@bp.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    username = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    if not title or not content:
        return jsonify({"msg": "title and content required"}), 400
    encrypted = encrypt_bytes(content.encode("utf-8"))
    notes_table.put_item(
        Item={
            "username": username,    # partition key
            "title": title,          # sort key
            "content": encrypted.hex(),  # store bytes as hex string
            "created_at": str(datetime.datetime.utcnow())
        }
    )
    return jsonify({"msg": "saved"}), 200

@bp.route("/notes/<title>", methods=["GET"])
@jwt_required()
def get_note_route(title):
    username = get_jwt_identity()
    resp = notes_table.get_item(Key={"username": username, "title": title})
    item = resp.get("Item")
    if not item:
        return jsonify({"msg": "not found"}), 404
    encrypted = bytes.fromhex(item["content"])
    decrypted = decrypt_bytes(encrypted).decode("utf-8")
    return jsonify({"title": title, "content": decrypted}), 200

@bp.route("/notes/<title>/upload", methods=["POST"])
@jwt_required()
def upload_file(title):
    username = get_jwt_identity()
    file = request.files.get("file")
    if not file:
        return jsonify({"msg": "No file uploaded"}), 400
    file_bytes = file.read()  # bytes
    encrypted_bytes = encrypt_bytes(file_bytes)
    bucket = os.getenv("S3_BUCKET")
    key = f"{username}/{title}/{file.filename}"
    upload_file_bytes(bucket, key, encrypted_bytes)

    return jsonify({"msg": "File uploaded successfully"}), 200

@bp.route("/")
def index():
    return "SafeNote is running!"