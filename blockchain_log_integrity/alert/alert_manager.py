import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import shutil

ALERT_DIR = "alerts"
ALERT_FILE = os.path.join(ALERT_DIR, "alerts.log")
SEALED_LEDGER_DIR = "ledger/sealed"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "blockchainalertmail@gmail.com"
EMAIL_PASSWORD = "zosgizdlxxqxlvdm"
EMAIL_RECEIVER = "prakashnp132@gmail.com"

def init_alert_dirs():
    os.makedirs(ALERT_DIR, exist_ok=True)
    os.makedirs(SEALED_LEDGER_DIR, exist_ok=True)

def log_alert(message: str):
    init_alert_dirs()
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(ALERT_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def send_email_alert(subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

def seal_ledger(ledger_path: str):
    if not os.path.exists(ledger_path):
        return False

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    sealed_path = os.path.join(
        SEALED_LEDGER_DIR, f"ledger_tampered_{timestamp}.enc"
    )
    shutil.move(ledger_path, sealed_path)
    return True

def raise_alert(reason: str, ledger_path: str = None):
    log_alert(reason)

    subject = "SECURITY ALERT: Blockchain Log Integrity Violation"
    body = f"""
ALERT TYPE: Log Integrity Violation

REASON:
{reason}

ACTION:
- Ledger sealed
- New ledger initialized

TIME:
{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
"""

    try:
        send_email_alert(subject, body)
    except Exception as e:
        log_alert(f"Email delivery failed: {str(e)}")

    if ledger_path:
        seal_ledger(ledger_path)
