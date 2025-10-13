import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("ENCRYPTION_KEY")
if not KEY:
    raise RuntimeError("ENCRYPTION_KEY not set in .env")

cipher = Fernet(KEY.encode() if isinstance(KEY, str) else KEY)

def encrypt_text(plaintext: str) -> str:
    return cipher.encrypt(plaintext.encode()).decode()

def decrypt_text(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()