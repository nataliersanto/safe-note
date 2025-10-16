import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("ENCRYPTION_KEY")
if not KEY:
    raise RuntimeError("ENCRYPTION_KEY not set in .env")

cipher = Fernet(KEY.encode() if isinstance(KEY, str) else KEY)

def encrypt_bytes(data: bytes) -> bytes:
    """Encrypt raw bytes, returns encrypted bytes"""
    return cipher.encrypt(data)

def decrypt_bytes(data: bytes) -> bytes:
    """Decrypt encrypted bytes, returns original bytes"""
    return cipher.decrypt(data)