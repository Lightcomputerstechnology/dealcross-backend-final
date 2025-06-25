from fastapi import APIRouter, HTTPException, Request, Depends
from core.security import get_current_user
from models.user import User
from services.payment_gateways import (
    initiate_paystack_payment,
    initiate_flutterwave_payment,
    initiate_nowpayments_crypto
)

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("/card")
async def fund_wallet_card(request: Request, current_user: User = Depends(get_current_user)):
    data = await request.json()
    amount = float(data.get("amount", 0))
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # Example: choose Paystack for now
    tx = await initiate_paystack_payment(user=current_user, amount=amount)
    return {"status": "initiated", "payment_link": tx.get("authorization_url")}


@router.post("/bank")
async def fund_wallet_bank(request: Request, current_user: User = Depends(get_current_user)):
    data = await request.json()
    amount = float(data.get("amount", 0))
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # Use Flutterwave or Paystack virtual account feature
    tx = await initiate_flutterwave_payment(user=current_user, amount=amount, method="bank_transfer")
    return {"status": "initiated", "payment_details": tx}


@router.post("/crypto")
async def fund_wallet_crypto(request: Request, current_user: User = Depends(get_current_user)):
    data = await request.json()
    amount = float(data.get("amount", 0))
    crypto_type = data.get("crypto_type", "usdt")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # Use NowPayments
    tx = await initiate_nowpayments_crypto(user=current_user, amount=amount, crypto=crypto_type)
    return {"status": "initiated", "payment_link": tx.get("invoice_url")}
