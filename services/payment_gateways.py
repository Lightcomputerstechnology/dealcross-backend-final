# File: services/payment_gateways.py

import httpx
import os
from models.user import User

# Load from env or config\NPAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET")
FLUTTERWAVE_SECRET = os.getenv("FLW_SECRET")
NOWPAY_API_KEY = os.getenv("NOWPAY_API_KEY")


# ─────────────────────────────────────────────
# ✅ PAYSTACK STANDARD CARD PAYMENT
# ─────────────────────────────────────────────
async def initiate_paystack_payment(user: User, amount: float):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": user.email,
        "amount": int(amount * 100),  # Paystack expects kobo
        "callback_url": "https://yourdomain.com/payment/verify/paystack"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["data"]


# ─────────────────────────────────────────────
# ✅ FLUTTERWAVE BANK TRANSFER
# ─────────────────────────────────────────────
async def initiate_flutterwave_payment(user: User, amount: float, method="bank_transfer"):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {FLUTTERWAVE_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "tx_ref": f"FLW-{user.id}-{os.urandom(4).hex()}",
        "amount": str(amount),
        "currency": "USD",
        "redirect_url": "https://yourdomain.com/payment/verify/flutterwave",
        "payment_options": method,
        "customer": {
            "email": user.email,
            "name": user.full_name or user.username
        },
        "customizations": {
            "title": "Dealcross Wallet Funding",
            "logo": "https://yourdomain.com/logo.png"
        }
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["data"]


# ─────────────────────────────────────────────
# ✅ NOWPAYMENTS CRYPTO PAYMENT
# ─────────────────────────────────────────────
async def initiate_nowpayments_crypto(user: User, amount: float, crypto="usdt"):
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {
        "x-api-key": NOWPAY_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "price_amount": amount,
        "price_currency": "usd",
        "pay_currency": crypto,
        "order_id": f"CRYPTO-{user.id}-{os.urandom(4).hex()}",
        "order_description": f"Wallet funding for {user.email}",
        "ipn_callback_url": "https://yourdomain.com/payment/webhook/nowpayments",
        "success_url": "https://yourdomain.com/payment/success"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()["data"]
                                
