from cryptography.fernet import Fernet
import json

# Paths
LEDGER_FILE = "ledger/ledger.enc"
KEY_FILE = "crypto/ledger.key"

# Load key
with open(KEY_FILE, "rb") as kf:
    key = kf.read()

fernet = Fernet(key)

# Load encrypted ledger
with open(LEDGER_FILE, "rb") as lf:
    encrypted_data = lf.read()

# Decrypt
decrypted_data = fernet.decrypt(encrypted_data)

# Convert JSON
ledger = json.loads(decrypted_data.decode())

# Print nicely
print(json.dumps(ledger, indent=4))
