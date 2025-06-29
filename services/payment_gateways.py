import os
import httpx
from models.user import User
from project_config.dealcross_config import settings  # ✅ Use unified global settings

# ─────────────────────────────────────────────
# ✅ PAYSTACK STANDARD CARD PAYMENT
# ─────────────────────────────────────────────
async def initiate_paystack_payment(user: User, amount: float):
    """
    Initiate a Paystack card payment and return the authorization URL.
    """
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.paystack_secret}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": user.email,
        "amount": int(amount * 100),  # Paystack expects amount in kobo
        "callback_url": settings.paystack_callback,
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
    """
    Initiate a Flutterwave payment and return the payment link.
    """
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.flw_secret}",
        "Content-Type": "application/json"
    }
    payload = {
        "tx_ref": f"FLW-{user.id}-{os.urandom(4).hex()}",
        "amount": str(amount),
        "currency": "USD",
        "redirect_url": settings.flutterwave_callback,
        "payment_options": method,
        "customer": {
            "email": user.email,
            "name": user.full_name or user.username
        },
        "customizations": {
            "title": "Dealcross Wallet Funding",
            "logo": "https://dealcross.net/logo192.png"  # ✅ Replace with your real logo URL
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
    """
    Initiate a NowPayments crypto invoice and return the invoice URL.
    """
    url = "https://api.nowpayments.io/v1/invoice"
    headers = {
        "x-api-key": settings.nowpay_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "price_amount": amount,
        "price_currency": "usd",
        "pay_currency": crypto,
        "order_id": str(user.id),
        "order_description": user.email,
        "ipn_callback_url": settings.nowpay_callback,
        "success_url": "https://dealcross.net/payment/success"  # ✅ Replace with your real URL
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()["data"]
        return data["invoice_url"]