# routers/payments_flutterwave.py
from fastapi import APIRouter, Request, HTTPException
import httpx, os

router = APIRouter(prefix="/api/flutterwave", tags=["Payments"])

FLW_SECRET_KEY = os.getenv("FLW_SECRET_KEY")

@router.post("/verify")
async def verify_flutterwave_payment(request: Request):
    body = await request.json()
    transaction_id = body.get("transaction_id")

    if not transaction_id:
        raise HTTPException(status_code=400, detail="Missing transaction_id")

    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {"Authorization": f"Bearer {FLW_SECRET_KEY}"}

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)

    data = resp.json()
    if data["status"] != "success":
        raise HTTPException(status_code=400, detail="Payment not successful")

    # ✅ Extract and process data
    payment_data = data["data"]
    tx_ref = payment_data["tx_ref"]
    amount = payment_data["amount"]
    customer_email = payment_data["customer"]["email"]

    # TODO: Save to DB, credit wallet, etc.
    return {
        "message": "Payment verified successfully",
        "data": {
            "tx_ref": tx_ref,
            "amount": amount,
            "email": customer_email
        }
    }