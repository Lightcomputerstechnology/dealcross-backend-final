# ======================
# File: utils/twofactor.py (TOTP-based logic)
# ======================
import pyotp
import qrcode
import io
from fastapi.responses import StreamingResponse

def generate_totp_secret():
    return pyotp.random_base32()

def generate_qr_code(username: str, secret: str):
    totp_uri = pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name="Dealcross Admin")
    qr = qrcode.make(totp_uri)
    buf = io.BytesIO()
    qr.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

def verify_totp(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code)
