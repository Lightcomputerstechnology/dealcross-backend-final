import hmac
import hashlib
from fastapi import Request, HTTPException
from core.settings import settings  # ✅ Import the settings instance

async def verify_paystack_signature(request: Request):
    """Verify Paystack webhook signature using SHA512."""
    body = await request.body()
    received_signature = request.headers.get("x-paystack-signature")

    if not received_signature:
        raise HTTPException(status_code=400, detail="Missing Paystack signature.")

    expected = hmac.new(
        settings.paystack_secret.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(expected, received_signature):
        raise HTTPException(status_code=403, detail="Invalid Paystack signature.")


async def verify_flutterwave_signature(request: Request):
    """Verify Flutterwave webhook signature using SHA256."""
    body = await request.body()
    received_hash = request.headers.get("verif-hash")

    if not received_hash:
        raise HTTPException(status_code=400, detail="Missing Flutterwave signature.")

    computed_hash = hmac.new(
        settings.flw_secret.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise HTTPException(status_code=403, detail="Invalid Flutterwave signature.")


async def verify_nowpayments_signature(request: Request):
    """Verify NowPayments webhook signature using SHA512."""
    body = await request.body()
    received_sig = request.headers.get("x-nowpayments-sig")

    if not received_sig:
        raise HTTPException(status_code=400, detail="Missing NowPayments signature.")

    computed_sig = hmac.new(
        settings.nowpay_api_key.encode("utf-8"),
        msg=body,
        digestmod=hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(computed_sig, received_sig):
        raise HTTPException(status_code=403, detail="Invalid NowPayments signature.")