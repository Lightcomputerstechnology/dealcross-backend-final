# File: services/payment_gateways.py

import httpx
from models.user import User
from core.settings import settings

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
        "amount": int(amount * 100),  # Paystack expects amount in kobo
        "callback_url": "https://yourdomain.com/payment/verify/paystack"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()["data"]
        return data["authorization_url"]


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
        data = res.json()["data"]
        return data["link"]


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
        "order_id": f"{user.id}",
        "order_description": user.email,
        "ipn_callback_url": "https://yourdomain.com/webhooks/nowpayments",
        "success_url": "https://yourdomain.com/payment/success"
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()["data"]
        return data["invoice_url"]