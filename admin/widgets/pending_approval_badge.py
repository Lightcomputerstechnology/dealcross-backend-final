# File: admin/widgets/pending_approval_badge.py

from fastapi_admin.widgets import Widget
from starlette.requests import Request
from tortoise.expressions import Q
from models.pending_approval import PendingApproval

class PendingApprovalBadge(Widget):
    async def render(self, request: Request) -> str:
        count = await PendingApproval.filter(Q(status="pending")).count()
        return f"""
        <div style='background:#fff; padding:1rem; border-radius:8px; text-align:center; box-shadow:0 0 6px #ccc;'>
            <h3 style='margin:0; font-size:1.2rem;'>Pending Approvals</h3>
            <p style='font-size:2rem; font-weight:bold; color:#ff8800;'>{count}</p>
        </div>
        """