# File: utils/admin_wallet_logger.py

from decimal import Decimal
from models.admin_wallet import AdminWallet
from models.admin_wallet_log import AdminWalletLog
from models.user import User

async def log_admin_wallet_activity(
    amount: float,
    action: str,
    description: str,
    triggered_by: User = None
):
    """
    Logs all changes to AdminWallet including system-generated actions.
    Automatically updates the admin wallet balance (if not yet created).
    """
    amount = Decimal(amount)
    wallet = await AdminWallet.first()
    if not wallet:
        wallet = await AdminWallet.create(balance=0)

    # No balance change happens here — this is for logging only.
    await AdminWalletLog.create(
        amount=amount,
        action=action,
        description=description,
        admin_wallet=wallet,
        triggered_by=triggered_by
    )