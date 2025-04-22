# File: utils/fraud_detection.py

def basic_fraud_check(deal):
    """
    Basic fraud detection rule.
    Flags deals with suspicious characteristics.
    """

    # Example rule: flag any deal over $10,000
    if deal.amount > 10000:
        return True

    # Add more rules as needed

    return False
