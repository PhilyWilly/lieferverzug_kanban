import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

# Config from your .env
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 25))
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", 30))
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
USE_TLS = os.getenv("USE_TLS", "True").lower() == "true"

def send_email(to_address, subject, body, from_address=FROM_ADDRESS):
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
        if USE_TLS:
            server.starttls()
        # If auth is required, uncomment and fill in:
        # server.login(username, password)
        server.sendmail(from_address, [to_address], msg.as_string())

if __name__ == "__main__":
    send_email(
        to_address="konfigurator@rehatec.com",
        subject="Test email",
        body="Hello, this is a test email sent from Python."
    )