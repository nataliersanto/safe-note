import pytest
from app.encryption import encrypt_bytes, decrypt_bytes

def test_encrypt_decrypt_roundtrip():
    plaintext = "hello world"
    token = encrypt_bytes(plaintext.encode())  # encode string to bytes
    decrypted = decrypt_bytes(token).decode()  # decrypt returns bytes, decode to string
    assert decrypted == plaintext
