# File: services/fee_logic.py

def calculate_fee(user, action: str, base_amount: float) -> float:
    """
    Calculates platform fee based on user role and action.
    Admins are exempt from all fees.
    """
    role = user.role
    sales = float(user.cumulative_sales)

    if role == "admin":
        return 0.0

    if action == "funding":
        return base_amount * (0.02 if role == "user" else 0.015)

    elif action == "escrow":
        return base_amount * (0.03 if role == "user" else 0.02)

    elif action == "share_buy":
        return base_amount * (0.02 if role == "user" else 0.015)

    elif action == "share_sell":
        if sales < 1000:
            return 0.0
        return base_amount * (0.01 if role == "user" else 0.0075)

    return 0.0