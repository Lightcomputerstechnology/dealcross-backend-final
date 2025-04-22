# Core user-facing routes
from . import auth
from . import wallet
from . import deals
from . import disputes
from . import kyc
from . import upload
from . import notifications

# Admin-facing routes
from .admin import analytics
from .admin import charts
from .admin import fraud
from .admin import auditlog
from .admin import dealcontrol
from .admin import usercontrol

# Exported for app startup to auto-discover routes
__all__ = [
    "auth",
    "wallet",
    "deals",
    "disputes",
    "kyc",
    "upload",
    "notifications",
    "analytics",
    "charts",
    "fraud",
    "auditlog",
    "dealcontrol",
    "usercontrol"
]
