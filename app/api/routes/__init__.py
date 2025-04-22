# Import FastAPI Router directly (no submodules)
from fastapi import APIRouter

# Import each router individually (delayed to avoid circular imports)
def include_all_routes():
    from . import auth
    from . import wallet
    from . import deals
    from . import disputes
    from . import kyc
    from . import upload
    from . import notifications

    from .admin import analytics
    from .admin import charts
    from .admin import fraud
    from .admin import auditlog
    from .admin import dealcontrol
    from .admin import usercontrol

    # Collect all routers here
    routes = [
        auth.router,
        wallet.router,
        deals.router,
        disputes.router,
        kyc.router,
        upload.router,
        notifications.router,
        analytics.router,
        charts.router,
        fraud.router,
        auditlog.router,
        dealcontrol.router,
        usercontrol.router,
    ]
    return routes

# Expose only the function
__all__ = ["include_all_routes"]
