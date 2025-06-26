# utils/otp.py
import pyotp
from models.user import User

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def get_totp_uri(user: User, secret: str, issuer: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name=issuer)

def verify_totp_code(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)