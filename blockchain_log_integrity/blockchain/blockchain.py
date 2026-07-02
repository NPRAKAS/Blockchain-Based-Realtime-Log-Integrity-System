import json
import os
import hashlib
import time
from crypto.crypto_utils import encrypt_data, decrypt_data
from cryptography.fernet import InvalidToken

LEDGER_DIR = "ledger"
LEDGER_FILE = os.path.join(LEDGER_DIR, "ledger.enc")

class LedgerTamperedException(Exception):
    pass

class Blockchain:
    def __init__(self):
        os.makedirs(LEDGER_DIR, exist_ok=True)

        # AUTO-RECOVERY: Create new ledger if missing
        if not os.path.exists(LEDGER_FILE):
            self._create_genesis_block()

    def _calculate_hash(self, index, timestamp, log_hash, previous_hash):
        data = f"{index}{timestamp}{log_hash}{previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()

    def _create_genesis_block(self):
        genesis_block = [{
            "index": 0,
            "timestamp": time.time(),
            "log_hash": "GENESIS",
            "previous_hash": "0",
            "current_hash": self._calculate_hash(0, time.time(), "GENESIS", "0")
        }]
        self._write_chain(genesis_block)

    def _read_chain(self):
        if not os.path.exists(LEDGER_FILE):
            # Ledger was sealed → recreate safely
            self._create_genesis_block()

        try:
            with open(LEDGER_FILE, "rb") as f:
                encrypted_data = f.read()

            decrypted = decrypt_data(encrypted_data)
            return json.loads(decrypted.decode())

        except InvalidToken:
            raise LedgerTamperedException(
                "Encrypted blockchain ledger has been tampered with"
            )

        except Exception as e:
            raise LedgerTamperedException(
                f"Ledger read failure: {str(e)}"
            )

    def _write_chain(self, chain):
        data = json.dumps(chain, indent=4).encode()
        encrypted = encrypt_data(data)
        with open(LEDGER_FILE, "wb") as f:
            f.write(encrypted)

    def add_block(self, log_hash):
        chain = self._read_chain()
        last_block = chain[-1]

        index = last_block["index"] + 1
        timestamp = time.time()
        previous_hash = last_block["current_hash"]
        current_hash = self._calculate_hash(index, timestamp, log_hash, previous_hash)

        block = {
            "index": index,
            "timestamp": timestamp,
            "log_hash": log_hash,
            "previous_hash": previous_hash,
            "current_hash": current_hash
        }

        chain.append(block)
        self._write_chain(chain)
        return block
