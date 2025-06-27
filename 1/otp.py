# File: utils/otp.py

import pyotp

def generate_totp_secret():
    return pyotp.random_base32()

def generate_totp_uri(username: str, secret: str, issuer: str = "Dealcross"):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)

def verify_totp_code(secret: str, code: str):
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)
