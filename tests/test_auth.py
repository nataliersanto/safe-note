import pytest
from app.encryption import encrypt_text, decrypt_text

def test_encrypt_decrypt_roundtrip():
    plaintext = "hello world"
    token = encrypt_text(plaintext)
    assert decrypt_text(token) == plaintext
