from models.fee_transaction import FeeType  # ✅ Import FeeType Enum

def calculate_funding_fee(amount: float, user_tier: str) -> float:
    if user_tier == 'basic':
        return round(amount * 0.02, 2)  # 2% for basic users
    else:
        return round(amount * 0.015, 2)  # 1.5% for upgraded users


def calculate_escrow_fee(amount: float, user_tier: str) -> float:
    if user_tier == 'basic':
        return round(amount * 0.03, 2)  # 3%
    else:
        return round(amount * 0.02, 2)  # 2%


def calculate_share_buyer_fee(amount: float, user_tier: str) -> float:
    if user_tier == 'basic':
        return round(amount * 0.02, 2)
    else:
        return round(amount * 0.015, 2)


def calculate_share_seller_fee(amount: float, cumulative_sales: float, user_tier: str) -> float:
    if cumulative_sales < 1000:
        return 0.0
    else:
        if user_tier == 'basic':
            return round(amount * 0.01, 2)
        else:
            return round(amount * 0.0075, 2)


def apply_escrow_fee(db, user, deal_amount):
    from utils.admin_wallet import credit_admin_wallet
    from utils.fee_logger import log_fee_transaction

    fee = calculate_escrow_fee(deal_amount, user.tier)
    credit_admin_wallet(db, fee)
    log_fee_transaction(db, user.id, FeeType.escrow, fee)  # ✅ Use Enum
    return deal_amount - fee, fee


def apply_share_trade_fee(db, user, amount, role="buyer"):
    from utils.admin_wallet import credit_admin_wallet
    from utils.fee_logger import log_fee_transaction

    if role == "buyer":
        fee = calculate_share_buyer_fee(amount, user.tier)
        log_type = FeeType.share_buy  # ✅ Use Enum
    else:
        fee = calculate_share_seller_fee(amount, user.cumulative_sales, user.tier)
        user.cumulative_sales += amount
        db.commit()
        log_type = FeeType.share_sell  # ✅ Use Enum

    credit_admin_wallet(db, fee)
    log_fee_transaction(db, user.id, log_type, fee)

    return amount - fee, fee
