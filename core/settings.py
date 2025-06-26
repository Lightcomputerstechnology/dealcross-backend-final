# core/settings.py

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Payment API Keys
PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET")
FLUTTERWAVE_SECRET = os.getenv("FLW_SECRET")
NOWPAY_API_KEY = os.getenv("NOWPAY_API_KEY")

# You can add more settings here later, e.g.:
# DATABASE_URL = os.getenv("DATABASE_URL")