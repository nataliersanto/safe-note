import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models import get_note
from app.encryption import decrypt_bytes

username = "testuser"
title = "MyFirstNote"

note_bytes = get_note(username, title)
if not note_bytes:
    print("Note not found")
else:
    if isinstance(note_bytes, str):
        note_bytes = bytes.fromhex(note_bytes)  # only if stored as hex
    decrypted = decrypt_bytes(note_bytes).decode("utf-8")
    print("Decrypted content:", decrypted)