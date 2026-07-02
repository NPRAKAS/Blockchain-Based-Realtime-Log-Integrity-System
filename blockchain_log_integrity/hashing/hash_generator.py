import hashlib

def generate_hash(log_entry: str) -> str:
    """
    Generates SHA-256 hash for a given log entry.
    """
    sha256 = hashlib.sha256()
    sha256.update(log_entry.encode('utf-8'))
    return sha256.hexdigest()
