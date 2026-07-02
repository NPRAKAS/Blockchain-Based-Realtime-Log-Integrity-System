import time
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from hashing.hash_generator import generate_hash
from blockchain.blockchain import Blockchain, LedgerTamperedException
from verifier.integrity_verifier import IntegrityVerifier
from alert.alert_manager import raise_alert

LOG_FILE = "/var/log/auth.log"
LEDGER_PATH = os.path.join(PROJECT_ROOT, "ledger", "ledger.enc")

blockchain = Blockchain()
verifier = IntegrityVerifier()

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == LOG_FILE:
            try:
                with open(LOG_FILE, "r") as file:
                    lines = file.readlines()
                    if not lines:
                        return

                    log_entry = lines[-1].strip()
                    log_hash = generate_hash(log_entry)

                    block = blockchain.add_block(log_hash)

                    status, message = verifier.verify_chain()

                    print("\n[NEW LOG ENTRY]")
                    print(log_entry)
                    print("[BLOCK INDEX]", block["index"])
                    print("[INTEGRITY STATUS]")
                    print(message)
                    print("-" * 70)

            except LedgerTamperedException as e:
                print("\n[SECURITY ALERT]")
                print(str(e))
                raise_alert(str(e), LEDGER_PATH)
                print("[ACTION] Ledger sealed and reinitialized")
                print("-" * 70)

            except Exception as e:
                print("\n[UNEXPECTED ERROR]")
                print(str(e))
                print("-" * 70)

if __name__ == "__main__":
    print("[*] Real-time monitoring with alerting started...")

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path="/var/log/", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[*] Monitoring stopped.")

    observer.join()
