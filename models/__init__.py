"""
Load in dependency order so every FK target exists
before the module that references it is mapped.
"""

from .kyc                import KYCRequest
from .user               import User
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
# from .notification     import Notification  # enable later