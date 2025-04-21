import smtplib
from email.mime.text import MIMEText
import os

# Make sure you set these in your .env or environment variables
EMAIL_ADDRESS = os.getenv("DEALCROSS_EMAIL")
EMAIL_PASSWORD = os.getenv("DEALCROSS_PASSWORD")

def send_email(to: str, subject: str, body: str):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials are not set.")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, [to], msg.as_string())
        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email: {e}")
