# File: utils/email_sender.py

import smtplib
from email.message import EmailMessage
import os

def send_contact_email(name: str, email: str, message: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient_email = os.getenv("ADMIN_EMAIL", smtp_user)

    msg = EmailMessage()
    msg["Subject"] = f"New Contact Message from {name}"
    msg["From"] = f"Dealcross Support <{smtp_user}>"
    msg["To"] = recipient_email
    msg.set_content(f"From: {name} <{email}>\n\n{message}")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)