# ======================
# File: utils/email_2fa.py (Email OTP logic)
# ======================
import random
import redis.asyncio as redis
from fastapi_mail import FastMail, MessageSchema
from config import settings

r = redis.Redis(host="localhost", port=6379, db=0)

async def send_email_otp(user_email: str):
    code = str(random.randint(100000, 999999))
    await r.set(f"otp:{user_email}", code, ex=300)  # 5 minutes expiry

    message = MessageSchema(
        subject="Your Dealcross 2FA Code",
        recipients=[user_email],
        body=f"Your one-time verification code is: {code}",
        subtype="plain"
    )
    fm = FastMail(settings.email_conf)
    await fm.send_message(message)

async def verify_email_otp(user_email: str, code: str) -> bool:
    stored = await r.get(f"otp:{user_email}")
    return stored and stored.decode() == code
