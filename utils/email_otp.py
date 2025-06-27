# File: utils/email_otp.py

import random
from datetime import datetime, timedelta
from models.user import User
from utils.send_email import send_email  # ✅ assumes you have this helper

async def send_email_otp(user: User):
    otp = ''.join(random.choices("0123456789", k=6))
    user.otp_code = otp
    user.otp_expiry = datetime.utcnow() + timedelta(minutes=10)
    await user.save()

    subject = "Your Dealcross Login OTP"
    body = f"""
    Hello {user.username},

    Your One-Time Password (OTP) for login is: {otp}

    It will expire in 10 minutes.

    If you did not request this, please ignore this email.

    Thank you,
    The Dealcross Team
    """
    await send_email(to=user.email, subject=subject, body=body)