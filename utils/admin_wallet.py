from models.admin_wallet import AdminWallet

def credit_admin_wallet(db, fee_amount: float):
    wallet = db.query(AdminWallet).first()
    if wallet:
        wallet.balance += fee_amount
        db.commit()
