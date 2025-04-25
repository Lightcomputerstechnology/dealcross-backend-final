from .user            import User
from .deal            import Deal
from .wallet          import Wallet
from .share           import Share
from .dispute         import Dispute
from .escrow_tracker  import EscrowTracker
from .settings        import AppSettings
from .aiinsight       import AIInsight        # ← existing

# New imports for fees and admin earnings
from .fee_transaction import FeeTransaction
from .admin_wallet    import AdminWallet