# app/utils/notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.utils.config import ALERT_EMAIL, ALERT_EMAIL_PASSWORD

def send_alert(subject: str, message: str, to_email: str):
    """
    Send an email alert dynamically to the given email.
    - subject: Email subject
    - message: Email body text
    - to_email: Recipient email (provided at runtime)
    """
    msg = MIMEMultipart()
    msg["From"] = ALERT_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(ALERT_EMAIL, ALERT_EMAIL_PASSWORD)
            server.send_message(msg)
            print(f"✅ Alert email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
