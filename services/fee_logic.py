# File: services/fee_logic.py

def calculate_fee(user, action: str, base_amount: float) -> float:
    """
    Calculates platform fee based on user role and action.
    - Admins pay no fees.
    - Users pay fixed rates or tier-based rates depending on action.
    """
    role = user.role
    sales = float(user.cumulative_sales)

    if role == "admin":
        return 0.0

    # Fixed 0.5% for all users
    if action == "funding":
        return base_amount * 0.005

    elif action == "escrow":
        return base_amount * 0.005

    elif action == "share_buy":
        return base_amount * 0.02 if role == "user" else base_amount * 0.015

    elif action == "share_sell":
        if sales < 1000:
            return 0.0
        return base_amount * 0.01 if role == "user" else base_amount * 0.007

    return 0.0
