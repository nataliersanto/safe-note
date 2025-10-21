import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.encryption import encrypt_bytes, decrypt_bytes

def test_encryption_decryption():
    original_text = "This is a secret note for testing!"
    print("Original text:", original_text)
    encrypted = encrypt_bytes(original_text.encode("utf-8"))
    print("Encrypted bytes:", encrypted)
    decrypted = decrypt_bytes(encrypted).decode("utf-8")
    print("Decrypted text:", decrypted)
    assert decrypted == original_text, "Decrypted text does not match original!"

if __name__ == "__main__":
    test_encryption_decryption()
    print("Encryption/decryption test passed!")
