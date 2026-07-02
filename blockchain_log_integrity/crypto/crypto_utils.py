from cryptography.fernet import Fernet
import os

KEY_FILE = "crypto/ledger.key"

def generate_key():
    os.makedirs("crypto", exist_ok=True)
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_data(data: bytes) -> bytes:
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_data(token: bytes) -> bytes:
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(token)
