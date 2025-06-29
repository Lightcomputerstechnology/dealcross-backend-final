# File: utils/otp.py

import pyotp

def generate_totp_secret():
    """Generate a random base32 TOTP secret."""
    return pyotp.random_base32()

def generate_totp_uri(username: str, secret: str, issuer: str = "Dealcross"):
    """Generate a TOTP provisioning URI for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=username, issuer_name=issuer)

def verify_totp_code(secret: str, code: str):
    """Verify a TOTP code with a window for slight time differences."""
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)