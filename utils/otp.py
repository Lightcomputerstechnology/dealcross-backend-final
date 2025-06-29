# File: utils/otp.py

import pyotp

def generate_totp_secret():
    """Generate a new TOTP base32 secret."""
    return pyotp.random_base32()

def generate_totp_uri(username: str, secret: str, issuer: str = "Dealcross"):
    """
    Generate a provisioning URI for the TOTP setup (QR code generation).
    Use this URI with Google Authenticator or Authy.
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)

def verify_totp_code(secret: str, code: str):
    """
    Verify a user-provided TOTP code with a 30-second window tolerance.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)