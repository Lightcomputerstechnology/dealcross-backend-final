"""
Import order chosen so every FK target table is already known
before the model that references it is mapped.
"""
from .kyc                import KYCRequest   # must come first (so users.id exists)
from .user               import User         # now can reference KYCRequest.user_id
from .deal               import Deal
from .wallet             import Wallet
from .wallet_transaction import WalletTransaction
from .share              import Share
from .dispute            import Dispute
from .escrow_tracker     import EscrowTracker
from .settings           import AppSettings
from .aiinsight          import AIInsight
from .fee_transaction    import FeeTransaction
from .admin_wallet       import AdminWallet
from .fraud              import FraudAlert
from .audit              import AuditLog
# from .notification     import Notification   # enable when ready