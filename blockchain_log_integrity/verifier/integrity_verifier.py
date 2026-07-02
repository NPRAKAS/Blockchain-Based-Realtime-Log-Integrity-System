import hashlib
from blockchain.blockchain import Blockchain, LedgerTamperedException

class IntegrityVerifier:
    def __init__(self):
        self.blockchain = Blockchain()

    def verify_chain(self):
        try:
            chain = self.blockchain._read_chain()

            for i in range(1, len(chain)):
                current = chain[i]
                previous = chain[i - 1]

                recomputed_hash = self._calculate_hash(
                    current["index"],
                    current["timestamp"],
                    current["log_hash"],
                    current["previous_hash"]
                )

                if current["current_hash"] != recomputed_hash:
                    return False, f"Block hash mismatch at index {current['index']}"

                if current["previous_hash"] != previous["current_hash"]:
                    return False, f"Hash chain broken at index {current['index']}"

            return True, "Blockchain integrity verified"

        except LedgerTamperedException as e:
            return False, str(e)

        except Exception as e:
            return False, f"Verification failure: {str(e)}"

    def _calculate_hash(self, index, timestamp, log_hash, previous_hash):
        data = f"{index}{timestamp}{log_hash}{previous_hash}"
        return hashlib.sha256(data.encode()).hexdigest()
